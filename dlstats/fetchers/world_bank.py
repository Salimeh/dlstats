
from dlstats.fetchers._skeleton import Skeleton, Category, Series, Dataset, Provider, CodeDict
from dlstats.fetchers.make_elastic_index import ElasticIndex
import io
import zipfile
import urllib.request
import xlrd
import datetime
import pandas
import pprint


class WorldBank(Skeleton):
    def __init__(self):
        super().__init__()         
        self.provider_name = 'WorldBank'
        self.provider = Provider(name=self.provider_name,website='http://www.worldbank.org/')
        
    def upsert_categories(self):
        document = Category(provider = self.provider_name, 
                            name = 'GEM' , 
                            categoryCode ='GEM')
        return document.update_database()

    def upsert_dataset(self, datasetCode):
        
        if datasetCode=='GEM':
            self.upsert_gem('http://siteresources.worldbank.org/INTPROSPECTS/Resources/' + \
                            'GemDataEXTR.zip',datasetCode)
        else:
            raise Exception("This dataset is unknown" + dataCode)
        es = ElasticIndex()
        es.make_index(self.provider_name,datasetCode)

    def upsert_gem(self, url, dataset_code):
        dataset = Dataset(self.provider_name,dataset_code)
        gem_data = GemData(dataset,url)
        dataset.name = 'Global Economic Monirtor'
        dataset.doc_href = 'http://data.worldbank.org/data-catalog/global-economic-monitor'
        dataset.last_update = gem_data.releaseDate
        dataset.series.data_iterator = gem_data
        dataset.update_database()

class GemData:
    def __init__(self,dataset,url):
        self.provider_name = dataset.provider_name
        self.dataset_code = dataset.dataset_code
        self.dimension_list = dataset.dimension_list
        self.attribute_list = dataset.attribute_list
        self.columns = iter([])
        self.sheets = iter([])
        self.response = urllib.request.urlopen(url)
        #Getting released date from headers of the Zipfile
        releaseDate = self.response.info()['Last-Modified'] 
        self.releaseDate = datetime.datetime.strptime(releaseDate, 
                                                      "%a, %d %b %Y %H:%M:%S GMT")
        self.zipfile = zipfile.ZipFile(io.BytesIO(self.response.read()))
        self.excel_filenames = iter(self.zipfile.namelist())
        self.freq_long_name = {'A': 'Annual', 'Q': 'Quarterly', 'M': 'Monthly', 'D': 'Daily'}
        
    def __iter__(self):
        return self

    def __next__(self):
        return(self.build_series())

    def build_series(self):
        try:
            column = next(self.columns)
        except StopIteration:
            self.update_sheet()
            column = next(self.columns)
        dimensions = {}
        col_header = self.sheet.cell_value(0,column)
        if self.series_name == 'Commodity Prices':
            dimensions['Commodity'] = self.dimension_list.update_entry('Commodity','',col_header) 
        else:    
            dimensions['Country'] = self.dimension_list.update_entry('Country','',col_header) 
        values = [str(v) for v in self.sheet.col_values(column,start_rowx=1)]
        release_dates = [self.lastUpdate for v in values]
        series_key = self.series_name.replace(' ','_').replace(',', '')
        # don't add a period if there is already one
        if series_key[-1] != '.':
            series_key += '.'
        series_key += col_header + '.' + self.frequency
        series = {}
        series['provider'] = self.provider_name
        series['datasetCode'] = self.dataset_code
        series['name'] = self.series_name + '; ' + col_header + '; ' + self.freq_long_name[self.frequency]
        series['key'] = series_key
        series['values'] = values
        series['attributes'] = {}
        series['dimensions'] = dimensions
        series['releaseDates'] = release_dates
        series['period_index'] = self.period_index
        series['revisions'] = []
        series['frequency'] = self.frequency
        return(series)
    
    def update_sheet(self):
        try:
            self.sheet = next(self.sheets)
        except StopIteration:
            self.update_file()
            self.sheet = next(self.sheets)
            
        self.columns = iter(range(1,self.sheet.row_len(0)))
        periods = self.sheet.col_slice(0, start_rowx=2)
        start_period = periods[0].value
        end_period = periods[-1].value
        print(self.series_name)
        print(self.sheet.name)
        if self.sheet.name == 'annual':    
            self.frequency = 'A'
            start_period = str(int(start_period))
            end_period = str(int(end_period))
        elif self.sheet.name == 'quarterly':    
            self.frequency = 'Q'
        elif self.sheet.name == 'monthly':    
            self.frequency = 'M'
            start_period = start_period.replace('M','-')
            end_period = end_period.replace('M','-')
        elif self.sheet.name == 'daily':    
            self.frequency = 'D'
            start_period = self.translate_daily_dates(start_period)
            end_period = self.translate_daily_dates(end_period)
        self.period_index = pandas.period_range(start_period,end_period, freq = self.frequency)

    def translate_daily_dates(self,value):
            date = xlrd.xldate_as_tuple(value,self.excel_book.datemode)
            return(pandas.Period(year=date[0],month=date[1],day=date[2],freq=self.frequency))
        
    def update_file(self):
        fname = next(self.excel_filenames)
        self.series_name = fname[:-5]
        self.lastUpdate = datetime.datetime(*self.zipfile.getinfo(fname).date_time[0:6])
        self.excel_book = xlrd.open_workbook(file_contents = self.zipfile.read(fname))
        self.sheets = iter([s for s in self.excel_book.sheets()
                            if s.name not in ['Sheet1','Sheet2','Sheet3','Sheet4',
                                              'Feuille1','Feuille2','Feuille3','Feuille4']])

if __name__ == "__main__":
    import world_bank
    w = world_bank.WorldBank()
    w.upsert_dataset('GEM')

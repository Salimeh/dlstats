# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 10:59:20 2015
@author: salimeh
"""

from dlstats.fetchers._commons import Fetcher, Categories, Series, Datasets, Providers, CodeDict, ElasticIndex
import urllib
import xlrd
import csv
import codecs
from datetime import datetime
import pandas
import pprint
from collections import OrderedDict
from re import match
from time import sleep
import requests
from lxml import etree
import re



class Esri(Fetcher):
    def __init__(self, db=None, es_client=None):
        super().__init__(provider_name='esri',  db=db, es_client=es_client)         
        self.provider_name = 'esri'
        self.provider = Providers(name=self.provider_name,
                                  long_name='Economic and Social Research Institute, Cabinet Office',
                                  region='Japan',
                                  website='http://www.esri.cao.go.jp/index-e.html',
                                  fetcher=self)

        #parsing the Esri page
        url = 'http://www.esri.cao.go.jp/en/sna/data/sokuhou/files/2015/qe152_2/gdemenuea.html'
        webpage = requests.get(url)
        html = etree.HTML(webpage.text)     
        tables = html.xpath("//table[@class = 'tableBase']")
        hrefs = tables[0].xpath (".//a")
        links = [href.values() for href in hrefs]
        gdp_urls = ['http://www.esri.cao.go.jp' + links[i][0][20:]  for i in range(8)]
        hrefs_ = tables[1].xpath(".//a")
        links_ = [href_.values() for href_ in hrefs_]
        deflator_urls = ['http://www.esri.cao.go.jp' + links_[2*i][0][20:]  for i in range(4)]
        self.url_all = gdp_urls + deflator_urls
        self.dataset_name_list = [ 'Nominal Gross Domestic Product (original series)',
                                   'Annual Nominal GDP (fiscal year)',                
                                   'Nominal Gross Domestic Product (seasonally adjusted series)',
                                   'Annual Nominal GDP (calendar year)',
                                   'Real Gross Domestic Product (original series)',
                                   'Annual Real GDP (fiscal year)',
                                   'Real Gross Domestic Product (seasonally adjusted series)',
                                   'Annual Real GDP (calendar year)',
                                   'Deflators (quarter:original series)',
                                   'Deflators (quarter:seasonally adjusted series)' ,
                                   'Deflators (fiscal year)',
                                   'Deflators (calendar year)']
        self.datasetCode_list = ['esri'+str(index+1) for index, s in enumerate(self.dataset_name_list)]
        self.dataset_name = {'esri' +str(index+1): s for index, s in enumerate(self.dataset_name_list)}
        #print(self.datasetCode_list)
        #print(self.dataset_name)
        
    def upsert_categories(self):
        document = Categories(provider = self.provider_name, 
                            name = 'esri', 
                            categoryCode ='esri',
                            children = None,
                            fetcher=self )
        return document.update_database()
        
    def esri_issue(self):
        for self.url in self.url_all :
            datasetCode = self.datasetCode_list[self.url_all.index(self.url)]
            self.upsert_dataset(datasetCode)

    def upsert_dataset(self, datasetCode):
        self.upsert_sna(self.url,datasetCode)                  
        self.update_metas(datasetCode)

    def upsert_sna(self, url, dataset_code):
        dataset = Datasets(self.provider_name,dataset_code,
                           fetcher=self)
        sna_data = EsriData(dataset,url)
        dataset.name = self.dataset_name[dataset_code]
        dataset.doc_href = 'http://www.esri.cao.go.jp/index-e.html'
        dataset.last_update = sna_data.release_date
        dataset.series.data_iterator = sna_data
        dataset.update_database()

    def upsert_all_datasets(self):
        self.upsert_categories()
        self.esri_issue()
        
class EsriData():
    def __init__(self,dataset,url):
        self.url = url
        self.provider_name = dataset.provider_name
        self.dataset_code = dataset.dataset_code
        self.dimension_list = dataset.dimension_list
        self.attribute_list = dataset.attribute_list
        self.panda_csv = self.get_csv_data(url)
        self.release_date = self.get_release_date()
        self.column_range = iter(range(1, self.panda_csv.shape[1]))
        self.currency = ''
        self.series_name = self.fix_series_names()
        
        if self.panda_csv.iloc[6,0] == '4' :
            self.frequency = 'A'
            ind = -1 
        else :
            self.frequency = 'Q'
            ind = -4
        end_date = self.panda_csv.iloc[self.panda_csv.shape[0]+ind,0][:4]
        start_date = self.panda_csv.iloc[6,0][:4]
        self.end_date = pandas.Period(end_date,freq = self.frequency).ordinal    
        self.start_date = pandas.Period(start_date,freq = self.frequency).ordinal
    
    def get_csv_data(self,url,**kwargs):
        return pandas.read_csv(url,**kwargs)
    
    def get_release_date(self):
        response = urllib.request.urlopen(self.url)
        releaseDate = response.info()['Last-Modified'] 
        return datetime.strptime(releaseDate,"%a, %d %b %Y %H:%M:%S GMT")                                                  
        
    def fix_series_names(self):
        #generating name of the series             
        columns =self.panda_csv.columns
        for column_ind in range(columns.size):
            if str(self.panda_csv.iloc[5,column_ind]) != "nan":
                #edit_nameseries = self.edit_seriesname(self.panda_csv.iloc[:,column_ind)[4])
                self.panda_csv.iloc[3,column_ind] = self.edit_seriesname(str(self.panda_csv.iloc[4,column_ind]))+', '+str(self.panda_csv.iloc[5,column_ind])
            else:    
                self.panda_csv.iloc[3,column_ind] = self.edit_seriesname(str(self.panda_csv.iloc[4,column_ind]))
            if str(self.panda_csv.iloc[4,column_ind]) == "nan" :
                if (str(self.panda_csv.iloc[5,column_ind]) != "nan") and (str(self.panda_csv.iloc[4,column_ind-1])) != "nan":         
                    self.panda_csv.iloc[3,column_ind] = self.edit_seriesname(str(self.panda_csv.iloc[4,column_ind-1]))+', '+str(self.panda_csv.iloc[5,column_ind])
                else:
                    if str(self.panda_csv.iloc[4,column_ind-1]) == "nan":
                        self.panda_csv.iloc[3,column_ind] = self.edit_seriesname(str(self.panda_csv.iloc[4,column_ind-2]))+', '+str(self.panda_csv.iloc[5,column_ind])  
            #Take into the account FISIM 
            if str(self.panda_csv.iloc[5,column_ind-1]) == "Excluding FISIM":
                self.panda_csv.iloc[3,column_ind] = self.edit_seriesname(str(self.panda_csv.iloc[4,column_ind]))+', '+str(self.panda_csv.iloc[5,column_ind-1])               
            if str(self.panda_csv.iloc[5,column_ind-2]) == "Excluding FISIM":
                self.panda_csv.iloc[3,column_ind] = self.edit_seriesname(str(self.panda_csv.iloc[4,column_ind]))+', '+str(self.panda_csv.iloc[5,column_ind-2])
            if str(self.panda_csv.iloc[5,column_ind-3]) == "Excluding FISIM":
                self.panda_csv.iloc[3,column_ind] = self.edit_seriesname(str(self.panda_csv.iloc[4,column_ind]))+', '+str(self.panda_csv.iloc[5,column_ind-3])
                
        lent = self.panda_csv.shape[1]
        if str(self.panda_csv.iloc[0,:][lent-1]) == "(%)":
            self.currency = str(self.panda_csv.iloc[0,lent-2])
        else:
            self.currency = str(self.panda_csv.iloc[0,lent-1])
        series_name = self.panda_csv.iloc[3,1:]
        return series_name
        
    def edit_seriesname(self,seriesname):   
         seriesname = seriesname.replace(' ','')  
         seriesname = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', seriesname)
         seriesname = re.sub(r"((of)|(in) |(from/to))", r" \1 ", seriesname)  
         seriesname = re.sub(r"(&)", r" \1 ", seriesname)
         seriesname = re.sub(r"(\()", r" \1", seriesname) 
         seriesname = seriesname.replace('  ',' ')
         return(seriesname)  
        
        
    def __next__(self):
        column = self.panda_csv.iloc[:,next(self.column_range)]
        #print(str(column[3]))
        if (str(column[3]) == "nan, nan") or (str(column[3]) == "nan" ) :
            column = self.panda_csv.iloc[:,next(self.column_range)]
        if column is None:
            raise StopIteration()
        series = self.build_series(column)
        if series is None:
            raise StopIteration()            
        return(series) 
           
                                           
    def build_series(self,column):
        
        dimensions = {}
        series = {}
        series_value = []       
        series_name = str(column[3])+'_ ' + self.frequency +'_ ' +self.currency
        series_key = 'esri.' + str(column[3]) + '; ' + self.frequency
        print('**************')        
        print(column[3])
        
       # print('**************')
        dimensions['concept'] = self.dimension_list.update_entry('concept','',str(column[3]))
        #print(dimensions['concept'])
        for r in range(6, len(column)):
            series_value.append(str(column[r]))    
        #release_dates = [self.releaseDate for v in series_value] 
        series['values'] = series_value                
        series['provider'] = self.provider_name       
        series['datasetCode'] = self.dataset_code
        series['name'] = series_name
        series['key'] = series_key
        series['startDate'] = self.start_date
        series['endDate'] = self.end_date  
        series['lastUpdate'] = self.release_date
        series['dimensions'] = dimensions
        series['frequency'] = self.frequency
        series['attributes'] = {}
        return(series)

if __name__ == "__main__":
    e = Esri()
    e.provider.update_database()
    e.upsert_all_datasets()
    e.upsert_categories()
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from collections import OrderedDict
from pprint import pprint
import time
import logging
import zipfile

import requests

from dlstats.fetchers._commons import Fetcher, Datasets, Providers
from dlstats.utils import Downloader
from dlstats.xml_utils import XMLData_1_0_FED as XMLData

VERSION = 1

logger = logging.getLogger(__name__)

DATASETS = {
    'G19': {
        "name": "G.19 - Consumer Credit",
        "doc_href": None,
        'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=G19&filetype=zip',
    },
    'Z17':{
         "name": "G.17 - Industrial Production and Capacity Utilization",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=G17&filetype=zip',
    },
    'H3':{
         "name": "H.3 - Aggregate Reserves of Depository Institution and the Monetary Base",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=H3&filetype=zip',
    },    
    'H8':{
         "name": "H.8 - Assets and Liabilities of Commercial Banks in the U.S.",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=H8&filetype=zip',
    },
    'E2':{
         "name": "E.2 - Survey of Terms of Business Lending",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=E2&filetype=zip',
    },
    'G20':{
         "name": "G.20 - Finance Companies",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=G20&filetype=zip',
    },
    'G5/H10':{
         "name": "G.5 / H.10 - Foreign Exchange Rates",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=H10&filetype=zip',
    },
    'Z1': {
        "name": "Z.1 - Financial Accounts of the United States",
        "doc_href": None,
        'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=Z1&filetype=zip',
    },    
    'H15':{
         "name": "H.15 - Selected Interest Rates",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=H15&filetype=zip',
    },
    'H41':{
         "name": "H.4.1 - Factors Affecting Reserve Balances",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=H41&filetype=zip',
    },
    'H6':{
         "name": "H.6 - Money Stock Measures",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=H6&filetype=zip',
    },
    'SLOOS':{
         "name": "SLOOS - Senior Loan Officer Opinion Survey on Bank Lending Practices",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=SLOOS&filetype=zip',
    },    
    'CP':{
         "name": "CP - Commercial Paper",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=CP&filetype=zip',
    },    
    'PRATES':{
         "name": "PRATES - Policy Rates",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=PRATES&filetype=zip',
    },
    'FOR':{
         "name": "FOR - Household Debt Service and Financial Obligations Ratios",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=FOR&filetype=zip',
    }, 
    'CHGDEL':{
         "name": "CHGDEL - Charge-off and Delinquency Rates",
         "doc_href": None,
         'url': 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=CHGDEL&filetype=zip ',
    },           
}
CATEGORIES = [
    {
        "category_code": "PEI",
        "name": "Principal Economic Indicators",
        "position": 1,
        "doc_href": None,
        "datasets": [
            {
                "dataset_code": "G19",
                "name": DATASETS["G19"]["name"], 
                "doc_href": DATASETS["G19"]["doc_href"], 
            },
            {
                "dataset_code": "G17",
                "name": DATASETS["G17"]["name"], 
                "doc_href": DATASETS["G17"]["doc_href"], 
            },
        ]
    },
    {
        "category_code": "BAL",
        "name": "Bank Assets & Liabilities",
        "position": 2,
        "doc_href": None,
        "datasets": [
            {
                "dataset_code": "H3",
                "name": DATASETS["H3"]["name"], 
                "doc_href": DATASETS["H3"]["doc_href"], 
            },
            {
                "dataset_code": "H8",
                "name": DATASETS["H8"]["name"], 
                "doc_href": DATASETS["H8"]["doc_href"], 
            },
            {
                "dataset_code": "CHGDEL",
                "name": DATASETS["CHGDEL"]["name"], 
                "doc_href": DATASETS["CHGDEL"]["doc_href"], 
            },              
            {
                "dataset_code": "SLOOS",
                "name": DATASETS["SLOOS"]["name"], 
                "doc_href": DATASETS["SLOOS"]["doc_href"], 
            },  
            {
                "dataset_code": "E2",
                "name": DATASETS["E2"]["name"], 
                "doc_href": DATASETS["E2"]["doc_href"], 
            },          
        ]
    },
    {
        "category_code": "BF",
        "name": "Business Finance",
        "position": 3,
        "doc_href": None,
        "datasets": [
            {
                "dataset_code": "CP",
                "name": DATASETS["CP"]["name"], 
                "doc_href": DATASETS["CP"]["doc_href"], 
            },
            {
                "dataset_code": "G20",
                "name": DATASETS["G20"]["name"], 
                "doc_href": DATASETS["G20"]["doc_href"], 
            },            
        ]
    },
    {
        "category_code": "ERID",
        "name": "Exchange Rates and International Data",
        "position": 4,
        "doc_href": None,
        "datasets": [
            {
                "dataset_code": "G5/H10",
                "name": DATASETS["G5/H10"]["name"], 
                "doc_href": DATASETS["G5/H10"]["doc_href"], 
            },           
        ]
    },
    {
        "category_code": "FA",
        "name": "Financial Accounts",
        "position": 5,
        "doc_href": None,
        "datasets": [
            {
                "dataset_code": "Z1",
                "name": DATASETS["Z1"]["name"], 
                "doc_href": DATASETS["Z1"]["doc_href"], 
            },
        ]
    },    
    {
        "category_code": "HF",
        "name": "Household Finance",
        "position": 6,
        "doc_href": None,
        "datasets": [
            {
                "dataset_code": "G19",
                "name": DATASETS["G19"]["name"], 
                "doc_href": DATASETS["G19"]["doc_href"], 
            },  
            {
                "dataset_code": "G20",
                "name": DATASETS["G20"]["name"], 
                "doc_href": DATASETS["G20"]["doc_href"], 
            }, 
            {
                "dataset_code": "FOR",
                "name": DATASETS["FOR"]["name"], 
                "doc_href": DATASETS["FOR"]["doc_href"], 
            },             
        ]
    }, 
    {
        "category_code": "IA",
        "name": "Industrial Activity",
        "position": 7,
        "doc_href": None,
        "datasets": [
            {
                "dataset_code": "G17",
                "name": DATASETS["G17"]["name"], 
                "doc_href": DATASETS["G17"]["doc_href"], 
            },           
        ]
    },   
    {
        "category_code": "IR",
        "name": "Interest Rates",
        "position": 8,
        "doc_href": None,
        "datasets": [
            {
                "dataset_code": "H15",
                "name": DATASETS["H15"]["name"], 
                "doc_href": DATASETS["H15"]["doc_href"], 
            },  
            {
                "dataset_code": "PRATES",
                "name": DATASETS["PRATES"]["name"], 
                "doc_href": DATASETS["PRATES"]["doc_href"], 
            },             
        ]
    }, 
    {
        "category_code": "MSRB",
        "name": "Money Stock and Reserve Balances",
        "position": 9,
        "doc_href": None,
        "datasets": [
            {
                "dataset_code": "H3",
                "name": DATASETS["H3"]["name"], 
                "doc_href": DATASETS["H3"]["doc_href"], 
            },  
            {
                "dataset_code": "H41",
                "name": DATASETS["H41"]["name"], 
                "doc_href": DATASETS["H41"]["doc_href"], 
            },   
            {
                "dataset_code": "H6",
                "name": DATASETS["H6"]["name"], 
                "doc_href": DATASETS["H6"]["doc_href"], 
            },              
        ]
    }      
    
]



def extract_zip_file(zipfilepath):
    zfile = zipfile.ZipFile(zipfilepath)
    filepaths = []
    for filename in zfile.namelist():
        if filename.endswith("struct.xml") or filename.endswith("data.xml"):
            filepath = zfile.extract(filename, os.path.dirname(zipfilepath))
            filepaths.append(os.path.abspath(filepath))
            #filepaths.update({filename: zfile.extract(filename, os.path.dirname(zipfilepath))})
    return sorted(filepaths)

class FED(Fetcher):
    
    def __init__(self, db=None, **kwargs):        
        super().__init__(provider_name='FED', db=db, **kwargs)
        
        self.provider = Providers(name=self.provider_name,
                                  long_name='Federal Reserve',
                                  version=VERSION,
                                  region='US',
                                  website='http://www.federalreserve.gov',
                                  fetcher=self)

    def build_data_tree(self, force_update=False):
        
        if self.provider.count_data_tree() > 1 and not force_update:
            return self.provider.data_tree

        for category_code, dataset in DATASETS.items():
            category_key = self.provider.add_category({"name": dataset["name"],
                                                       "category_code": category_code,
                                                       "doc_href": dataset["doc_href"]})
            _dataset = {"name": dataset["name"], "dataset_code": category_code}
            self.provider.add_dataset(_dataset, category_key)
        
        return self.provider.data_tree

    def upsert_dataset(self, dataset_code):
        
        start = time.time()
        logger.info("upsert dataset[%s] - START" % (dataset_code))
        
        #TODO: control si existe ou update !!!

        dataset = Datasets(provider_name=self.provider_name, 
                           dataset_code=dataset_code,
                           name=DATASETS[dataset_code]['name'],
                           doc_href=DATASETS[dataset_code]['doc_href'],
                           last_update=datetime.now(),
                           fetcher=self)
        
        _data = FED_Data(dataset=dataset, 
                         url=DATASETS[dataset_code]['url'])
        dataset.series.data_iterator = _data
        result = dataset.update_database()
        
        _data = None

        end = time.time() - start
        logger.info("upsert dataset[%s] - END - time[%.3f seconds]" % (dataset_code, end))
        
        return result

    def load_datasets_first(self):
        start = time.time()        
        logger.info("datasets first load. provider[%s] - START" % (self.provider_name))
        
        self.provider.update_database()
        self.upsert_data_tree()

        datasets_list = [d["dataset_code"] for d in self.datasets_list()]
        for dataset_code in datasets_list:
            try:
                self.upsert_dataset(dataset_code)
            except Exception as err:
                logger.fatal("error for dataset[%s]: %s" % (dataset_code, str(err)))

        end = time.time() - start
        logger.info("datasets first load. provider[%s] - END - time[%.3f seconds]" % (self.provider_name, end))

    def load_datasets_update(self):
        #TODO: 
        self.load_datasets_first()

class FED_Data(object):
    
    def __init__(self, dataset=None, url=None):
        """
        :param Datasets dataset: Datasets instance
        """        
        self.dataset = dataset
        self.url = url
        self.attribute_list = self.dataset.attribute_list
        self.dimension_list = self.dataset.dimension_list
        self.provider_name = self.dataset.provider_name
        self.dataset_code = self.dataset.dataset_code

        #self.xml_dsd = XMLStructure_2_1(provider_name=self.provider_name, 
        #                                dataset_code=self.dataset_code)        
        
        self.rows = None
        #self.dsd_id = None
        
        self._load()
        
        
    def _load(self):

        download = Downloader(url=self.url, 
                              filename="data-%s.xml" % self.dataset_code,
                              #headers=SDMX_DATA_HEADERS        
                              )
        data_fp, dsd_fp = (extract_zip_file(download.get_filepath()))

        self.xml_data = XMLData(provider_name=self.provider_name,
                                dataset_code=self.dataset_code,
                                #dimension_keys=self.xml_dsd.dimension_keys
                                )
        
        self.rows = self.xml_data.process(data_fp)

    def __next__(self):
        _series = next(self.rows)
        if not _series:
            raise StopIteration()
        
        return self.build_series(_series)

    def build_series(self, bson):
        bson["last_update"] = self.dataset.last_update
        
        for key, item in bson['dimensions'].items():
            self.dimension_list.update_entry(key, key, item)

        return bson
        


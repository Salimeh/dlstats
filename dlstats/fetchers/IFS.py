# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 16:22:46 2015

@author: salimeh
"""


import csv
import pandas


class IFS_Data():
    def __init__(self):
        self.original_data = {}
        self.d = []
        self.key_all= []
        self.red = []
        self.attempt = {}
        self.country_list= {}
        self.indicatore_list= {}
    def load_original_data(self):
        
        with open('/home/salimeh/IFS/IFS_300.csv') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader :
                print(row)
                
                self.frequency = 'A'
                if 'Q' in row["Time Period"]:
                    self.frequency = 'Q'
                if 'M' in row["Time Period"]: 
                    self.frequency = 'M'                   
                self.key = row["Indicator Code"]+'.'+row["Country Code"] +'.'+ self.frequency 
                if self.key in self.attempt.keys():

                    self.attempt[self.key]["Country Code"] = row["Country Code"]
                    self.attempt[self.key]["Indicator Code"] = row["Indicator Code"]
                    self.attempt[self.key]["frequency"] =self.frequency
                    self.attempt[self.key]["values"][pandas.Period(row["Time Period"],self.frequency).ordinal+23] = row["Value"]
                    self.attempt[self.key]["Status"][pandas.Period(row["Time Period"],self.frequency).ordinal+23] = row["Status"]
                
                else:
                    self.attempt[self.key] = {}
                    self.attempt[self.key]["values"] =  ["na" for i in range(2015-1947)]
                    self.attempt[self.key]["Status"] =  ["na" for i in range(2015-1947)]
                    if self.frequency == 'M':                 
                        self.attempt[self.key]["values"] =  ["na" for i in range(12*(2015-1947))]
                        self.attempt[self.key]["Status"] =  ["na" for i in range(12*(2015-1947))]
                    if self.frequency == 'Q':
                        self.attempt[self.key]["values"] =  ["na" for i in range(4*(2015-1947))]
                        self.attempt[self.key]["Status"] =  ["na" for i in range(4*(2015-1947))]
                        
                    self.attempt[self.key]["Country Code"] = row["Country Code"]
                    self.attempt[self.key]["Indicator Code"] = row["Indicator Code"]
                    self.attempt[self.key]["frequency"] =self.frequency
                    #print(self.attempt[self.key]["values"])
                    #print(self.frequency)
                    print(row["Time Period"])
                    #print(pandas.Period(row["Time Period"],self.frequency).ordinal+23+1947)
                    self.attempt[self.key]["values"][pandas.Period(row["Time Period"],self.frequency).ordinal+23] = row["Value"]
                    self.attempt[self.key]["Status"][pandas.Period(row["Time Period"],self.frequency).ordinal+23] = row["Status"]
                print(row["Country Name"])
                if row["Country Code"] in self.country_list.keys():
                    break
                else:
                    self.country_list[row["Country Code"]] =  row["Country Name"]               
                    

                if row["Indicator Code"] in self.indicatore_list.keys():
                    break
                else:    
                    self.indicatore_list[row["Indicator Code"]] = row["Indicator Name"]
                    

        

        return(self.attempt)
if __name__ == "__main__":
    w = IFS_Data()
    ee= w.load_original_data()
    
        
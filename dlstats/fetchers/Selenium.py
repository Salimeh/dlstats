# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:38:00 2015

@author: salimeh
"""

#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()
browser.get('https://www.bookstore.imf.org/authgatewaylogin?ssortn=http%3a%2f%2fdata.imf.org%2f%3fsk%3d5DABAFF2-C5AD-4D27-A175-1253419C02D1')


#binary = FirefoxBinary("/opt/firefox30.0/firefox")
#browser = webdriver.Firefox(firefox_binary=binary)
#browser.get('https://www.bookstore.imf.org/authgatewaylogin?ssortn=http%3a%2f%2fdata.imf.org%2f%3fsk%3d5DABAFF2-C5AD-4D27-A175-1253419C02D1')

username = selenium.find_element_by_id("Email:")
password = selenium.find_element_by_id("password")

username.send_keys("widukind-info@cepremap.org")
password.send_keys("rdBs!2iA")
page = selenium.find_element_by_name("submit").click()

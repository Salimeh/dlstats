===============
imf
===============

Provider
========

:provider_name: IMF
:provider_longname: International Monetary Fund 
:provider URL: http://www.imf.org/
:approximate number of datasets: 2 (WEO and IFS)

Data accessibility
==================

:API: API SDMX-XML 2.0 et 2.1 We are discussing about that in issue #28
:API main URL:http://datahelp.imf.org/knowledgebase/articles/630877-data-services
:Datafiles: yes
:Datafile format: WEO are available in csv file , IFS is Zip file of csv (2.7 G)

Desired datasets
================

:Description: WEO and IFS


Data tree
=========

:Existence of a hierarchy of datasets on web site: No
:How to recover the information: for WEO: http://www.imf.org/external/ns/cs.aspx?id=28 , For IFS we need to creat an account for Bulk download, http://data.imf.org/?sk=5DABAFF2-C5AD-4D27-A175-1253419C02D1
Datasets
========

:datasetCode: provided, WEO and IFS
:how to get release date: For WEO we can get it in the related Url to download the file. For IFS we use the date of the file in its headers.
:dataset docHref: no
:dataset notes: no
:dimension_list: to be made up from the series
:use of attributes: WEO : yes, IFS: No
:attribute_list: to be made up from the series 
:available frequencies: WEO: Annual, IFS: Annual, Quarterly, Monthly
:availability of previous updates: WEO : yes the archives are avaiable in the website. http://www.imf.org/external/ns/cs.aspx?id=28 , IFS: No
:existence of real time datasets: NO
Series
======

:Series key: WEO: row['WEO Subject Code']+'.'+row['ISO']+'.'+dimensions['Units'], IFS: row['Indicator Code']
:Series name: to be made up, WEO : row['Subject Descriptor']+'.'+row['Country']+'.'+row['Units'], IFS: row['Indicator Name']+'.'+row['Country Name']
:Series docHref: No
:Series notes: No
:missing values: No
:date format: 
:mixed frequencies in the same dataset: NO for WEO, yes for IFS

Updates
=======

:calendar of future updates: No
:summary of previous upudates: WEO :http://www.imf.org/external/ns/cs.aspx?id=28, IFS: No 
:regular updates: WEO: 2 times in the year, usually October and April the day is not fixed.
:RSS flow:
:best way to monitor updates: WEO: checking the mentioned URL, IFS: checking the date of the Zipped file 
Special problems
================
Creating an account for bulk downloading of IFS is necessary. Also for IFS we have Time period column. The date is organized in the different way. We have to read all data once and organized it according to the date and after insert the series in Mongo. By now, we assumed same starting and ending date for all series but apparently it is not the case. In addition, the zip file is around 3 Gigabite, therefore the time issue might be important in reading IFS.

Other remarks
=============

Data samples
============

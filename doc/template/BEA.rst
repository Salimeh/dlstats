===============
BEA
===============

Provider
========

:provider_name: BEA
:provider_longname: Bureau of American Analysis 
:provider URL: http://www.bea.gov/
:approximate number of datasets: 3 main groups(National Data, Industry Data and International Data), each of them contains 2 main subgroups. In each subgroups we have different sections and in each sections there is more than 30 datasets. 

Data accessibility
==================

:API: Is avaiable to registered users on the BEA public web site. API guid: http://www.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf, (Registration link:http://www.bea.gov/api/signup/)
:API main URL:http://www.bea.gov/api/data
:Datafiles: yes
:Datafile format: csv, xls, zipped xls nd ziped csv 

Desired datasets
================

:Description: We are interested in National Data, Industry Data and International Data main groups


Data tree
=========

:Existence of a hierachy of datasets on web site: National Data (first level)
GDP and personal income(Second level)
Section1: Domestic product and income (third level )
Tables Sheets (Forth level)
Section2: Personal income and outlays(third level )
Section3: Government current receipts and expenditures(third level )
Section4: Foreign transactions(third level )
Section5: Saving and investment(third level )
Section6: Income and employment by industry(third level )
Section7: Supplemental tables(third level )
Fixed Assets Accounts tables(Second level)
Section1: Fixed assets and consumer Durable goods(third level )
Section2: Private fixed assets by type(third level )
Section3: Private fixed assets by industry(third level )
Section4: Nonresidential fixed assets(third level )
Section5: Residential fixed assets(third level )
Section6: Private fixed assets(third level )
Section7: Governmental fixed assets(third level )
Section8: Consumer durable goods(third level )
Section9: Chained dollar tables(third level )
Industry Data(first level)
GDP-by-industry(Second level)
Value added by industry(A,Q)(third level )
Gross output by industry(A,Q)(third level )
intermediate input by industry(A,Q)(third level )
Input-Output(Second level)
Use table(third level )
make table(third level )
Direct requierments(third level )
Total requirments(third level )
International Data(first level)
Int'Transactions, Services & IIP(Second level)
International transactions(ITA)(third level )
International services(third level )
International investment position(IIP)(third level )
Direct investment & MNEs ()(Second level)
U.S. Direct Investment Abroad:(third level )
Balance of payments and direct investment position data
Data on the activities of U.S. multinational enterprises
Foreign Direct Investment in the United States:
Balance of payments and direct investment position data
Data on the activities of U.S affiliates of foreign multinational enterprises

:How to recover the information: http://www.bea.gov//national/nipaweb/DownSS2.asp#ZXLS, 
http://www.bea.gov//national/FA2004/DownSS2.asp
http://www.bea.gov//industry/iTables%20Static%20Files/AllTables.zip
http://www.bea.gov//industry/iTables%20Static%20Files/AllTablesQTR.zip
http://www.bea.gov//industry/iTables%20Static%20Files/AllTablesIO.zip
http://www.bea.gov/international/bp_web/tb_download_type_modern.cfm?list=1&RowID=0
http://www.bea.gov/international/bp_web/tb_download_type_modern.cfm?list=4&RowID=0
http://www.bea.gov/international/bp_web/tb_download_type_modern.cfm?list=5&RowID=0
http://www.bea.gov/international/di1usdbal.htm
http://www.bea.gov/international/di1usdop.htm
http://www.bea.gov/international/di1fdibal.htm
http://www.bea.gov/international/di1fdiop.htm



Datasets
========

:datasetCode: (provided or to be made up, suggest scheme if necessary)
:how to get release date: In each xls sheet: Data published November 25, 2015 and File created 11/24/2015 11:44:04 AM
:dataset docHref: no
:dataset notes: yes
:dimension_list: (provided or to be made up from the series)
:use of attributes: no
:attribute_list: 
:available frequencies: Annual, Quarterly and Monthly
:availability of previous updates: No
:existence of real time datasets: No
Series
======

:Series key: sheet name
:Series name: second element of each row + frequency
:Series docHref: no
:Series notes: yes(Same for all series, better to put it in datasets notes)
:missing values: code for missing values
:date format: String
:mixed frequencies in the same dataset: no

Updates
=======

:calendar of future updates: No
:summary of previous updates: if yes, provide URL 
:regular updates: date and time
:RSS flow:
:best way to monitor updates: 	     
		     
Special problems
================
To have dataset name we have to open the xls or csv file. because the sheet name in datasets here.
If we keep line as a series name, we can not keep the data in the same format of the data sourse. 
for example we will loose Addena in the following example. But some time we are obliged to keep the line which is ''. Because it is an explanation about the serie, for example:
26	  Less: Administrative expenses	                                                            
	  Effect of participation in defined contribution plans on personal income, saving, and wealth:	 
27	  Effect on personal income (1-9-10 or 15-9-10)	                                              
28	  Less: Effect on personal consumption expenditures (2)	
29	  Equals: Effect on personal saving	
30	  Plus: Holding gains and other changes in assets	
31	  Equals: Change in personal wealth	


Released date dose not keep in same cell in all xls file.
Monthly data has a different template, the data are arranged in different lines.

For Direct investment & MNEs there is not a direct line.
Other remarks
=============

Data samples
============
Example of monthly data
Line			                                             1969	     1969	     1969
			                                               1 	       2	      3
1	   Personal consumption expenditures (PCE)	DPCERC1	584.2	589.5	589.7
2	Goods	                                   DGDSRC1	297.4	300.0	299.1
3	  Durable goods	                         DDURRC1	90.1	     90.8	     89.1
4	  Nondurable goods	                         DNDGRC1	207.3	209.3	209.9
5	Services	                                   DSERRC1	286.8	289.4	290.6
	Addenda:	 			
6	  PCE excluding food and energy	          DPCCRC1	454.1	458.2 	457.9
7	  Food \1\	                              DFXARC1	92.8	     93.3	     93.1
8	  Energy goods and services \2\	          DNRGRC1	37.4	     37.9	     38.7
9	  Market-based PCE \3\	                    DPCMRC1	.....	.....	.....
10	  Market-based PCE excluding food and \3\	DPCXRC1	.....	.....	.....
					
1. Food consists of food and beverages purchased for off-premises consumption; food services, which					
include purchased meals and beverages, are not classified as food.					
2. Consists of gasoline and other energy goods and of electricity and gas services.					
3. Market-based PCE is a supplemental measure that is based on household expenditures for which there					
are observable price measures. It excludes most imputed transactions (for example, financial services					
furnished without payment) and the final consumption expenditures of nonprofit institutions serving					
households.

Line			                                              1986	1986	  1986
			                                                1	       2	    3
1	   Personal consumption expenditures (PCE)	  DPCERC1	2,838.3	2,831.2	2,834.7
2	Goods	                                     DGDSRC1	1,185.8	1,166.0	1,160.8
3	  Durable goods	                           DDURRC1	401.4	389.4	384.1
4	  Nondurable goods	                           DNDGRC1	784.4	776.7	776.7
5	Services	                                     DSERRC1	1,652.5	1,665.2	1,673.9
	Addenda:	 			
6	  PCE excluding food and energy	            DPCCRC1	2,325.3	2,321.8	2,333.2
7	  Food \1\	                                DFXARC1	314.5	313.5	315.5
8	  Energy goods and services \2\	            DNRGRC1	198.5	195.9	186.0
9	  Market-based PCE \3\	                      DPCMRC1	.....	.....	.....
10	  Market-based PCE excluding food and \3\	  DPCXRC1	.....	.....	.....
					
1. Food consists of food and beverages purchased for off-premises consumption; food services, which					
include purchased meals and beverages, are not classified as food.					
2. Consists of gasoline and other energy goods and of electricity and gas services.					
3. Market-based PCE is a supplemental measure that is based on household expenditures for which there					
are observable price measures. It excludes most imputed transactions (for example, financial services					
furnished without payment) and the final consumption expenditures of nonprofit institutions serving					


					

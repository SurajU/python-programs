# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 10:16:37 2019

@author: Suraj
"""

# This script scrapes information on specialists working in hospitals. Given the 
# setup of the website, detailed information on specialists can only be obtained 
# if you search for specific specialists, such as by name or AGB-code. This 
# script first gets these basic info and then gets detailed info by looping 
# through all the specialists collected in the first part.

from selenium import webdriver
import os
import time
import pandas as pd
import math
from Check_Chromedriver import Check_Chromedriver
import shutil


try:
    os.chdir("C:/Users/u1272934/surfdrive/webscraping")
except:
    os.chdir("C:/Users/Suraj/surfdrive/webscraping")
    
    
Check_Chromedriver.main()
shutil.copyfile('.\\chromedriver\\chromedriver.exe','.\\chromedriver.exe')

# before getting specialist data, need to get all hospitals in NL.
listHosp = pd.read_csv("allHospitals.csv", header = 0)
    
browser = webdriver.Chrome()
url = "https://www.agbcode.nl/Webzoeker/Zoeken"
browser.get(url)
browser.find_element_by_xpath('//*[@id="geavZoeken"]/form/div/center/table/tbody/tr[1]/td[2]/input[2]').click()
browser.find_element_by_xpath("//select[@name='ZorgsoortVeldOnd']/option[text()='06 - Ziekenhuizen']").click()

nRows = 0
writer = pd.ExcelWriter("allSpecialists.xlsx",engine='openpyxl')

for eachHosp in range(0,len(listHosp)):
    
    typeInField = browser.find_element_by_id("AGBCodeVeld")
    typeInField.clear()
    typeInField.send_keys(str(listHosp.iloc[eachHosp]['INSTELLING_AANGELEVERD']))
    browser.find_element_by_id("bttnZoeken").click()
    time.sleep(2)
    browser.find_elements_by_xpath("//table[@id='dataTable']//td[@class='sorting_1']")[0].click()
    allInformationInPage = pd.read_html(browser.page_source)

    openRelatieTab = browser.find_elements_by_xpath("/html/body/div/div[2]/div/div[2]/table/tbody/tr/td/div/div[2]/h3[1]/span")
    openRelatieTab[0].click()
    
    time.sleep(1)
    
    try:
        getPageNo = browser.find_element_by_id("DataTables_Table_0_info")
    except: 
        continue
    
    numberOfPages = getPageNo.text
    numberOfPages = numberOfPages.split()
    numberOfPages = numberOfPages[-1]
    numberOfPages = numberOfPages.replace(',','')
    numberOfPages = math.ceil(int(numberOfPages[:-1])/100)
    
    for eachPage in range(0,numberOfPages):
        browser.find_element_by_xpath("//select[@name='DataTables_Table_0_length']/option[text()='100']").click()
        time.sleep(2)
        allInformationInPage = pd.read_html(browser.page_source)
        tableWithSpecialistData = allInformationInPage[2]
        tableWithSpecialistData = tableWithSpecialistData.iloc[:-1,2:]
        addAGBCode = listHosp.iloc[eachHosp]
        addAGBCode = addAGBCode.repeat(repeats = len(tableWithSpecialistData)).reset_index(drop=True)
    
        finalTable = pd.concat([addAGBCode,tableWithSpecialistData], axis = 1, join='inner')
        finalTable.to_excel(writer,header=False,index=False,startrow=nRows)
        
        nRows = nRows + len(tableWithSpecialistData)
        
        if eachPage < numberOfPages:
            browser.find_element_by_id("DataTables_Table_0_next").click()
            time.sleep(2)
    
    browser.find_element_by_class_name("terugPijlImg").click()
    time.sleep(2)

writer.save()
writer.close()

###############################################################################
# after getting all specialists, get their work status
###############################################################################
listSpec = pd.read_excel("allSpecialists.xlsx",header = None)
listRelSpec = pd.DataFrame(listSpec[1])
listRelSpec[2] = listRelSpec[1].astype(str).str[0]
onlyMedSpec = listRelSpec[listRelSpec[2] == '3'] 
onlyMedSpec = onlyMedSpec.drop_duplicates()

listSpec = onlyMedSpec[1].astype(str).str[:-2]
listSpec = listSpec.reset_index(drop = True)

browser = webdriver.Chrome()
url = "https://www.agbcode.nl/Webzoeker/Zoeken"
browser.get(url)
browser.find_element_by_xpath("//select[@name='ZorgsoortVeldZvl']/option[text()='03 - Medisch Specialisten']").click()

time.sleep(2)

writer = pd.ExcelWriter("whereProvidersWork2.xlsx",engine='openpyxl')

nRows = 0

for eachSpecialist in range(19987,len(listSpec)):
    
    try:
        typeInField = browser.find_element_by_id("AGBCodeVeld")
        typeInField.clear()
        typeInField.send_keys(listSpec[eachSpecialist])
        browser.find_element_by_id("bttnZoeken").click()
        time.sleep(2)
        
    except: 
        time.sleep(20)
        browser.refresh()
        time.sleep(2)
        browser.get(url)
        browser.find_element_by_xpath("//select[@name='ZorgsoortVeldZvl']/option[text()='03 - Medisch Specialisten']").click()
        time.sleep(2)
        typeInField = browser.find_element_by_id("AGBCodeVeld")
        typeInField.clear()
        typeInField.send_keys(listSpec[eachSpecialist])
        browser.find_element_by_id("bttnZoeken").click()
        time.sleep(2)
    
    try:    
        browser.find_elements_by_xpath("//table[@id='dataTable']//td[@class='sorting_1']")[0].click()
    except:
        continue
    
    allInformationInPage = pd.read_html(browser.page_source)
    
    tableToExtract = allInformationInPage[2]
    tableToExtract = tableToExtract.iloc[0:,2:]
    
    try:
        qualificationTable = pd.concat([allInformationInPage[5]]*len(tableToExtract), ignore_index = True)    
    except: 
        qualificationTable = pd.concat([allInformationInPage[3]]*len(tableToExtract), ignore_index = True)    
        
    addAGBCode = pd.Series(listSpec[eachSpecialist])
    addAGBCode = addAGBCode.repeat(repeats = len(tableToExtract)).reset_index(drop=True)
    
    finalTable = pd.concat([addAGBCode,tableToExtract,qualificationTable], axis = 1, join='inner')
    finalTable.to_excel(writer,header=False,index=False,startrow=nRows)
    
    browser.find_element_by_class_name("terugPijlImg").click()
    time.sleep(2)
    nRows = nRows + len(tableToExtract)
    
writer.save()
writer.close()

###############################################################################
# Do the same for ZBCs
###############################################################################

try:
    os.chdir("C:/Users/u1272934/surfdrive/webscraping")
except:
    os.chdir("C:/Users/Suraj/surfdrive/webscraping")
    
# before getting specialist data, need to get all specialists in NL
listHosp = pd.read_csv("allZBCsInData.csv", header = 0)
    
browser = webdriver.Chrome()
url = "https://www.agbcode.nl/Webzoeker/Zoeken"
browser.get(url)
browser.find_element_by_xpath('//*[@id="geavZoeken"]/form/div/center/table/tbody/tr[1]/td[2]/input[2]').click()
browser.find_element_by_xpath("//select[@name='ZorgsoortVeldOnd']/option[text()='22 - Zelfstandige Behandelcentra']").click()

nRows = 0
writer = pd.ExcelWriter("allSpecialistsZBC.xlsx",engine='openpyxl')

for eachHosp in range(477,len(listHosp)):
    
    typeInField = browser.find_element_by_id("AGBCodeVeld")
    typeInField.clear()
    typeInField.send_keys(str(listHosp.iloc[eachHosp]['INSTELLING_AANGELEVERD']))
    browser.find_element_by_id("bttnZoeken").click()
    time.sleep(2)
    
    try:
        browser.find_elements_by_xpath("//table[@id='dataTable']//td[@class='sorting_1']")[0].click()
    except:
        continue

    allInformationInPage = pd.read_html(browser.page_source)

    openRelatieTab = browser.find_elements_by_xpath("/html/body/div/div[2]/div/div[2]/table/tbody/tr/td/div/div[2]/h3[1]/span")
    openRelatieTab[0].click()
    
    time.sleep(1)
    
    try:
        getPageNo = browser.find_element_by_id("DataTables_Table_0_info")
    except: 
        browser.find_element_by_class_name("terugPijlImg").click()
        time.sleep(2)
        continue
    
    numberOfPages = getPageNo.text
    numberOfPages = numberOfPages.split()
    numberOfPages = numberOfPages[-1]
    numberOfPages = numberOfPages.replace(',','')
    numberOfPages = math.ceil(int(numberOfPages[:-1])/100)
    
    for eachPage in range(0,numberOfPages):
        browser.find_element_by_xpath("//select[@name='DataTables_Table_0_length']/option[text()='100']").click()
        time.sleep(2)
        allInformationInPage = pd.read_html(browser.page_source)
        tableWithSpecialistData = allInformationInPage[2]
        tableWithSpecialistData = tableWithSpecialistData.iloc[:-1,2:]
        addAGBCode = listHosp.iloc[eachHosp]
        addAGBCode = addAGBCode.repeat(repeats = len(tableWithSpecialistData)).reset_index(drop=True)
    
        finalTable = pd.concat([addAGBCode,tableWithSpecialistData], axis = 1, join='inner')
        finalTable.to_excel(writer,header=False,index=False,startrow=nRows)
        
        nRows = nRows + len(tableWithSpecialistData)
        
        if eachPage < numberOfPages:
            browser.find_element_by_id("DataTables_Table_0_next").click()
            time.sleep(2)
    
    browser.find_element_by_class_name("terugPijlImg").click()
    time.sleep(2)

writer.save()
writer.close()


###############################################################################
# get the type of specialist work for ZBC specialists
###############################################################################

listSpec = pd.read_excel("allSpecialistsZBC.xlsx",header = None)
listRelSpec = pd.DataFrame(listSpec[1])
listRelSpec[2] = listRelSpec[1].astype(str).str[0]
onlyMedSpec = listRelSpec[listRelSpec[2] == '3'] 
onlyMedSpec = onlyMedSpec.drop_duplicates()

listSpec = onlyMedSpec[1].astype(str)
listSpec = listSpec.reset_index(drop = True)

browser = webdriver.Chrome()
url = "https://www.agbcode.nl/Webzoeker/Zoeken"
browser.get(url)
browser.find_element_by_xpath("//select[@name='ZorgsoortVeldZvl']/option[text()='03 - Medisch Specialisten']").click()

time.sleep(2)

writer = pd.ExcelWriter("whereProvidersWorkZBCWithQualifications.xlsx",engine='openpyxl')

nRows = 0

for eachSpecialist in range(0,len(listSpec)):
    
    try:
        typeInField = browser.find_element_by_id("AGBCodeVeld")
        typeInField.clear()
        typeInField.send_keys(listSpec[eachSpecialist])
        browser.find_element_by_id("bttnZoeken").click()
        time.sleep(2)
        
    except: 
        time.sleep(20)
        browser.refresh()
        time.sleep(2)
        browser.get(url)
        browser.find_element_by_xpath("//select[@name='ZorgsoortVeldZvl']/option[text()='03 - Medisch Specialisten']").click()
        time.sleep(2)
        typeInField = browser.find_element_by_id("AGBCodeVeld")
        typeInField.clear()
        typeInField.send_keys(listSpec[eachSpecialist])
        browser.find_element_by_id("bttnZoeken").click()
        time.sleep(2)
    
    try:    
        browser.find_elements_by_xpath("//table[@id='dataTable']//td[@class='sorting_1']")[0].click()
    except:
        continue
    
    allInformationInPage = pd.read_html(browser.page_source)
    
    tableToExtract = allInformationInPage[2]
    tableToExtract = tableToExtract.iloc[0:,2:]
        
    qualificationTable = pd.concat([allInformationInPage[5]]*len(tableToExtract), ignore_index = True)
    
    addAGBCode = pd.Series(listSpec[eachSpecialist])
    addAGBCode = addAGBCode.repeat(repeats = len(tableToExtract)).reset_index(drop=True)
    
    finalTable = pd.concat([addAGBCode,tableToExtract,qualificationTable], axis = 1, join='inner')
    finalTable.to_excel(writer,header=False,index=False,startrow=nRows)
    
    browser.find_element_by_class_name("terugPijlImg").click()
    time.sleep(2)
    nRows = nRows + len(tableToExtract)
    
writer.save()
writer.close()

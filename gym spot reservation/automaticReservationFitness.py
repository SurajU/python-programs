# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 16:40:41 2020

@author: u1272934
"""

# This file just simulates clicking behavior to reserve a gym spot.
# This code does not work anymore. The website for the sports center at 
# Tilburg University underwent a major overhaul in the last year.

from selenium import webdriver
import os
import time
from Check_Chromedriver import Check_Chromedriver
import shutil
from datetime import date
import numpy as np

os.chdir("C:\\Users\\suraj\\surfdrive\\other stuff")

# make sure version of chrome driver matches version of chrome
Check_Chromedriver.main()

shutil.copyfile('.\\chromedriver\\chromedriver.exe','.\\chromedriver.exe')


browser = webdriver.Chrome()
timeSleep = 5

url = "https://tilburguniversity.sports.delcom.nl/pages/login"
browser.get(url)
time.sleep(timeSleep)

browser.find_element_by_xpath('//*[@id="third_providers_ul"]/li[1]').click()
time.sleep(timeSleep)

browser.find_element_by_xpath('//*[@id="idp-picker"]/section[2]/ul/li[2]').click()
time.sleep(timeSleep)

uNameIn = "u1272934"
passwordIn = "[INSERT PASSWORD HERE]"

browser.find_element_by_xpath('//*[@id="username"]').send_keys(uNameIn)
browser.find_element_by_xpath('//*[@id="password"]').send_keys(passwordIn)

browser.find_element_by_name('login').click()

browser.find_element_by_xpath('//*[@id="footer"]/div[1]/div[1]/ul/li[2]/a').click()
time.sleep(timeSleep)

browser.find_element_by_xpath('//*[@id="groupId"]/option[@value = "Fitness"]').click()
time.sleep(timeSleep)

browser.find_element_by_xpath('//*[@id="iResourceID"]/option[2]').click()
time.sleep(timeSleep)

browser.find_element_by_xpath('//*[@id="calendar"]/table/tbody/tr/td[1]/span[2]/span').click()
time.sleep(timeSleep)

# book the gym on Mon, Tue, Thur and Fri.
daysToBookGym = [0,1,3,4]
dayToday = date.today().weekday()

# the only difference in XPath across days is one number.
changeXPath = np.array([9,21,45,55])

# choose the correct XPath based on the day it runs. This chooses a slot a week
# in advance.
chooseXPath = np.repeat(dayToday,len(daysToBookGym)) == daysToBookGym

finalXPath = '//*[@id="calendar"]/div/div/div/div/div/div/div'+str(changeXPath[chooseXPath])+'/div[1]/div[1]/div'

browser.find_element_by_xpath(finalXPath).click()
time.sleep(timeSleep)

browser.find_element_by_xpath('//*[@id="addBookingButton"]').click()

time.sleep(timeSleep)
browser.quit()
#   
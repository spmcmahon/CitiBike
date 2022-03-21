# Scraping Citi Bike for CSV files 

import time
from selenium.webdriver.common.by import By
from selenium import webdriver 



pathtodriver = '/Applications/chromedriver'

#  Connecting to CitiBike Web Page 
driver = webdriver.Chrome(pathtodriver)
driver.get('https://s3.amazonaws.com/tripdata/index.html')

# Finding and downloading each zip file 

time.sleep(1)
lines = driver.find_elements_by_xpath("//a")
for x in lines:
    x.click()


# Extracting and Removing csv and zip folders
​
import os
from zipfile import ZipFile
​
# Jersey City ZIPS

source = '/Users/mcmahon/Documents/CitiBike2/JerseyCity/'
​
​
for file in os.listdir(source):
    if file.endswith('.zip'):
        file_name = source + file
        zip_ref = ZipFile(file_name)
        zip_ref.extractall(source)
        os.remove(file_name)
​
​
​
# NYC ZIPS
​
source2 = '/Users/mcmahon/Documents/CitiBike2/NewYork/'

for file in os.listdir(source2):
    if file.endswith('.zip'):
        file_name = source2 + file
        zip_ref = ZipFile(file_name)
        zip_ref.extractall(source2)
        os.remove(file_name) 
​
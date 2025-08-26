import os
import time
import pickle
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
load_dotenv()

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.linkedin.com")
time.sleep(3)

with open("linkedin_cookies.pkl", "rb") as f:
    cookies = pickle.load(f)
    for cookie in cookies:
        if 'sameSite' in cookie and cookie['sameSite'] == 'None':
            cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)
driver.refresh()

base_url = "https://www.linkedin.com/jobs/search/"
params = {
    "distance": 100,
    "f_TPR": "r86400",  # last 24 hours
    "geoId": 102713980, # India
    "keywords": "python developer"
}
url = f"{base_url}?{urlencode(params)}"
driver.get(url)


element1 = driver.find_element(By.CLASS_NAME, "scaffold-layout__list") # scaffold-layout__list
element2 = driver.find_element(By.CLASS_NAME, "scaffold-layout__detail") # scaffold-layout__detail
# element3 = driver.find_element(By.CLASS_NAME, "mt4") # mt4

while True:
    print(element1.text)
    print("\n\n\n\n")
    with open("jobDetail.txt", "w+", encoding="utf-8") as file:
        file.write(element2.text)
    print(element2.text)
    time.sleep(300)
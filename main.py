import os
import time
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
load_dotenv()

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.linkedin.com")

with open("linkedin_cookies.pkl", "rb") as f:
    cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)

url = "https://www.linkedin.com/jobs/search-results/?distance=100&f_TPR=r86400&geoId=102713980&keywords=python&origin=JOBS_HOME_SEARCH_BUTTON"
driver.get(url)

element1 = driver.find_element(By.CLASS_NAME, "jobs-semantic-search-list") # scaffold-layout__list
element2 = driver.find_element(By.CLASS_NAME, "jobs-semantic-search-detail") # scaffold-layout__detail

while True:
    print(element1.text)
    print("\n\n\n\n")
    with open("jobDetail.txt", "w+", encoding="utf-8") as file:
        file.write(element2.text)
    print(element2.text)
    time.sleep(300)
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

class Apply:
    def __init__(self):
        service = Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        self.driver = driver
        driver.maximize_window()

    def getLinkedin(self):
        self.driver.get("https://www.linkedin.com")
        time.sleep(3)
    
    def login(self):
        with open("linkedin_cookies.pkl", "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                if 'sameSite' in cookie and cookie['sameSite'] == 'None':
                    cookie['sameSite'] = 'Strict'
                self.driver.add_cookie(cookie)
        self.driver.refresh()

    def make_url(self, params):
        base_url = "https://www.linkedin.com/jobs/search/"
        url = f"{base_url}?{urlencode(params)}"
        self.url = url
        return url

    def go_to_jobs(self):
        self.driver.get(self.url)
        element1 = self.driver.find_element(By.CLASS_NAME, "scaffold-layout__list") # scaffold-layout__list
        element2 = self.driver.find_element(By.CLASS_NAME, "scaffold-layout__detail") # scaffold-layout__detail
        # element3 = self.driver.find_element(By.CLASS_NAME, "mt4") # mt4

    def get_application_link(self):
        apply_button = self.driver.find_element(By.ID, "jobs-apply-button-id")
        apply_button.click()
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[-1])
        # print("Application url:", self.driver.current_url)
        return self.driver.current_url
    
    def main(self, params):
        self.getLinkedin()
        self.login()
        self.make_url(params)
        self.go_to_jobs()
        application_link = self.get_application_link()
        print(application_link)

if __name__ == "__main__":
    while True:
        apply = Apply()
        params = {
                "distance": 100,
                "f_TPR": "r86400",  # last 24 hours
                "geoId": 102713980, # India
                "f_WT" : 2, # 1 for on-site, 2 for remote, 3 for hybrid
                "keywords": "python developer"
            }
        apply.main(params)
        time.sleep(3600)
    # while True:
        #     # print(element1.text)
        #     # print("\n\n\n\n")
        #     # with open("jobDetail.txt", "w+", encoding="utf-8") as file:
        #     #     file.write(element2.text)
        #     # print(element2.text)
        #     time.sleep(300)
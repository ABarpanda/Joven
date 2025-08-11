import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

options = Options()
options.add_argument("--headless=new")  # Now headless is fine ✅
options.add_argument("--disable-webrtc")
options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns,WebRTC")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
driver.get("https://www.linkedin.com")

# Load cookies
with open("linkedin_cookies.pkl", "rb") as f:
    cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)

# Go to feed or profile directly (you're now authenticated)
driver.get("https://www.linkedin.com/feed/")
time.sleep(2)
print("[+] Page title:", driver.title)

# Optionally visit a profile
profile_url = "https://www.linkedin.com/in/laxmimerit"
driver.get(profile_url)
time.sleep(2)
print("[+] Viewing profile:", driver.title)

driver.quit()
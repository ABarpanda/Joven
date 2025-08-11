import os
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()

# ❌ Don't use headless for 2FA
# options.add_argument("--headless=new")  

options.add_argument("--disable-webrtc")
options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns,WebRTC")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
driver.get("https://www.linkedin.com/login")

# Enter credentials
driver.find_element(By.ID, 'username').send_keys(os.environ['EMAIL'])
driver.find_element(By.ID, 'password').send_keys(os.environ['PASSWORD'])
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# 🔒 Now you're on the 2FA page — do it manually
print("[!] Waiting for you to complete 2FA in the open browser window...")

# Wait until redirected after 2FA (max 5 minutes)
WebDriverWait(driver, 300).until(EC.url_contains("/feed"))

print("[+] 2FA complete, now saving cookies...")

# Save cookies
with open("linkedin_cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print("[+] Done. Cookies saved.")
driver.quit()

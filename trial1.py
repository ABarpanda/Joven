import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

# Set up Chrome options
options = Options()
options.add_argument("--disable-webrtc")
options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns,WebRTC")
options.add_argument("--log-level=3")
# Comment out headless for manual 2FA
# options.add_argument("--headless=new")  # Disabled for 2FA input

# Initialize driver
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)

# Open LinkedIn login page
driver.get('https://www.linkedin.com/login')
print("[+] Page Title:", driver.title)

# Fill in credentials
driver.find_element(By.ID, 'username').send_keys(os.environ['EMAIL'])
driver.find_element(By.ID, 'password').send_keys(os.environ['PASSWORD'])
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Let page load (optional)
time.sleep(3)

# Navigate to a profile to ensure login success
profile_url = "https://www.linkedin.com/in/amritanshu-barpanda/"
driver.get(profile_url)
print("[+] Navigated to:", profile_url)
print("[+] Profile Title:", driver.title)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait up to 300 seconds (5 mins) for the profile page to load after 2FA
print("[!] Waiting for you to complete 2FA...")

WebDriverWait(driver, 300).until(
    EC.url_contains("/feed/")  # You can use '/feed/' or '/in/' depending on redirect
)

print("[+] 2FA complete. Saving cookies...")

# Save cookies
with open("linkedin_cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print("[+] Cookies saved.")
driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os

ENVIRONMENT = 'SERVER'

if ENVIRONMENT == 'SERVER':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    print(chrome_options)
    driver = webdriver.Chrome(chrome_options,os.environ.get("CHROMEDRIVER_PATH"),True)

if ENVIRONMENT == 'LOCAL':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

driver.get("https://agentweb2.plymouthrock.com/aiui/login")
print(driver.current_url)
driver.find_element(By.CSS_SELECTOR,'[id="j_username"]').send_keys('slopes_brz')
driver.find_element(By.CSS_SELECTOR,'[id="j_password"]').send_keys('As12!@RPA')
driver.find_element(By.CSS_SELECTOR,'[id="login"]').click()
sleep(3)
print(driver.current_url)


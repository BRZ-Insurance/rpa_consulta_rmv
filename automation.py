from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chromium import service
from time import sleep
import os


class BOT():
    def __init__(self) -> None:
        ENVIRONMENT = 'LOCAL'

        if ENVIRONMENT == 'SERVER':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_service =  service.ChromiumService(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
            self.driver = webdriver.Chrome(chrome_options,chrome_service,True)
            print('\nEXECUTEI\n')
            

        if ENVIRONMENT == 'LOCAL':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=chrome_options)
    
    def run(self,message):

        self.driver.get("https://agentweb2.plymouthrock.com/aiui/login")
        print(self.driver.current_url)
        self.driver.find_element(By.CSS_SELECTOR,'[id="j_username"]').send_keys('slopes_brz')
        self.driver.find_element(By.CSS_SELECTOR,'[id="j_password"]').send_keys('As12!@RPA')
        # driver.find_element(By.CSS_SELECTOR,'[id="login"]').click()
        sleep(3)
        print(message)
        print(self.driver.current_url)


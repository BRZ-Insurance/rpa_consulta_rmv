import automation
from collections.abc import Callable, Iterable, Mapping
from typing import Any
import threading
import time
from fastapi import FastAPI, Request
import json

##################
from selenium import webdriver
from selenium.webdriver.chromium import service
from time import sleep
import Email_API
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

##################
app = FastAPI()

class CustomThread(threading.Thread):
    def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,*self._kwargs)
        
    def join(self):
        threading.Thread.join(self)
        return self._return


#TODO implementar um meio de fazer rodar em ordem

###################################
ENVIRONMENT = 'SERVER'

if ENVIRONMENT == 'SERVER':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_service =  service.ChromiumService(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(chrome_options,chrome_service,True)
    print('\nEXECUTEI\n')
    

if ENVIRONMENT == 'LOCAL':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-dev-shm-usage")
    prefs = {"profile.managed_default_content_settings.images": 2} # desabilita o carregamento de imagens
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)


index_rpa = 2

if index_rpa == 0:
    name_rpa = 'rpa'
if index_rpa == 1:
    name_rpa = 'rpa1'
if index_rpa == 2:
    name_rpa = 'arp2'
if index_rpa == 3:
    name_rpa = 'arp3'
if index_rpa == 4:
    name_rpa = 'par4'
if index_rpa == 5:
    name_rpa = 'par5'
if index_rpa == 6:
    name_rpa = 'rap6'
if index_rpa == 7:
    name_rpa = 'rap7'
if index_rpa == 8:
    name_rpa = 'pra8'
if index_rpa == 9:
    name_rpa = 'pra9'

USERNAME = f'{name_rpa}@brzinsurance.com'
PASSWORD = 'M!QY7GfBMKhP&Mjr'

while True:
    try:
        driver.get("https://atlas-myrmv.massdot.state.ma.us/eservices/_/")
        print(driver.current_url)
        sleep(1)
        driver.find_element(By.CSS_SELECTOR,'[aria-label="Username"]').send_keys(USERNAME)
        driver.find_element(By.CSS_SELECTOR,'[aria-label="Password"]').send_keys(PASSWORD, Keys.ENTER)
        sleep(8)
        
        # TODO garantir que altera para cada index_rpa
        verification_code = Email_API.get_Verification_Code_RMV(index_rpa) # index_rpa
        
        driver.find_element(By.CSS_SELECTOR,'[type="text"]').send_keys(verification_code,Keys.ENTER)
        print('inseri o verification code e cliquei no ENTER')
        
        # TODO trocar a forma de avaliar se o verification code deu certo mesmo

        url = r'https://atlas-myrmv.massdot.state.ma.us/eservices/_/#2'
        print(url)
        n = 0
        while url == r'https://atlas-myrmv.massdot.state.ma.us/eservices/_/#2':
            sleep(1)
            driver.execute_script("document.querySelectorAll('span').forEach((e)=>{if(e.innerText == 'Search for a Vehicle'){e.click()}})")
            print('cliquei no Search Vehicles')
            url = driver.current_url
            print(url)
            n += 1
            if n == 3:
                sleep(1)
                verification_code = Email_API.get_Verification_Code_RMV(1) # index_rpa
                driver.find_element(By.CSS_SELECTOR,'[type="text"]').send_keys(verification_code,Keys.ENTER)
                print('inseri o verification code e cliquei no ENTER')
                sleep(2)


            
        break
    except Exception as error:
        print('nova tentativa')
        print('\n\n',error)
        sleep(9)

















########################################
@app.post('/carrier')
async def call_bot(request: Request):
    J = await request.json()

    bot = automation.BOT().run_carrier

    bot_runner = threading.Thread(target=bot,args=[J.get('url')])
    
    bot_runner.start()
    
    bot_runner.join()

    return 'executado'

@app.post('/rmv')
async def call_bot(request: Request):
    J = await request.json()

    # bot = automation.BOT().run_rmv
    bot = automation.BOT().run_rmv

    # bot_runner = threading.Thread(target=bot,args=[J.get('vin')])
    # bot_runner = CustomThread(target=bot,args=[J.get('vin')])
    bot_runner = CustomThread(target=bot,args=[J.get('vin'),driver])

    bot_runner.start()    
    
    super_json = bot_runner.join()

    return super_json
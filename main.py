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
from pydantic import BaseModel

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
driver_list = []
index_rpa = 0
n = 0

class VIN(BaseModel):
    vin: str

@app.post('/')
def init():
    
    global driver_list
    global index_rpa
    global n
    
    print(f'\nPARÂMETROS INICIAIS:\ndriver_list:{driver_list}\nindex_rpa:{index_rpa}\nn:{n}')
    ########################################
    ENVIRONMENT = 'LOCAL_CHROME'
    ########################################


    if ENVIRONMENT == 'SERVER_CHROME':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_service =  service.ChromiumService(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
        driver = webdriver.Chrome(chrome_options,chrome_service,True)
        print('\nEXECUTEI SERVER_CHROME\n')

    if ENVIRONMENT == 'SERVER_GECKO':
        from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.log.level = "trace"

        firefox_options.add_argument("-remote-debugging-port=9224")
        firefox_options.add_argument("-headless")
        firefox_options.add_argument("-disable-gpu")
        firefox_options.add_argument("-no-sandbox")

        binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))

        driver = webdriver.Firefox(firefox_binary=binary,executable_path=os.environ.get('GECKODRIVER_PATH'),options=firefox_options)
        print('\nEXECUTEI SERVER_GECKO\n')

    if ENVIRONMENT == 'LOCAL_CHROME':
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        prefs = {"profile.managed_default_content_settings.images": 2} # desabilita o carregamento de imagens
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=chrome_options)

    if ENVIRONMENT == 'LOCAL_GECKO':
        firefox_options = webdriver.FirefoxOptions()
        # chrome_options.add_argument("--headless")
        firefox_options.add_argument("-disable-dev-shm-usage")
        driver = webdriver.Firefox(options=firefox_options)

    # if index_rpa == 0:
    #     name_rpa = 'rpa'
    # if index_rpa == 1:
    #     name_rpa = 'rpa1'
    # if index_rpa == 2:
    #     name_rpa = 'arp2'
    # if index_rpa == 3:
    #     name_rpa = 'arp3'
    # if index_rpa == 4:
    #     name_rpa = 'par4'
    # if index_rpa == 5:
    #     name_rpa = 'par5'
    # if index_rpa == 6:
    #     name_rpa = 'rap6'
    # if index_rpa == 7:
    #     name_rpa = 'rap7'
    # if index_rpa == 8:
    #     name_rpa = 'pra8'
    # if index_rpa == 9:
    #     name_rpa = 'pra9'

    if index_rpa == 0:
        name_rpa = 'rpa1'
    if index_rpa == 1:
        name_rpa = 'arp2'
    if index_rpa == 2:
        name_rpa = 'arp3'
    if index_rpa == 3:
        name_rpa = 'par4'
    if index_rpa == 4:
        name_rpa = 'par5'
    if index_rpa == 5:
        name_rpa = 'rap6'
    if index_rpa == 6:
        name_rpa = 'rap7'
    if index_rpa == 7:
        name_rpa = 'pra8'
    if index_rpa == 8:
        name_rpa = 'pra9'
    if index_rpa == 9:
        name_rpa = 'rpa'

    
    if index_rpa == 10:
        index_rpa = 0

    USERNAME = f'{name_rpa}@brzinsurance.com'
    PASSWORD = 'M!QY7GfBMKhP&Mjr'
    INDEX = index_rpa
    index_rpa += 1

    
    driver.get("https://atlas-myrmv.massdot.state.ma.us/eservices/_/")
    print('\n',driver.current_url,'\n',index_rpa)
    sleep(1)
    driver.find_element(By.CSS_SELECTOR,'[aria-label="Username"]').send_keys(USERNAME)
    driver.find_element(By.CSS_SELECTOR,'[aria-label="Password"]').send_keys(PASSWORD,Keys.ENTER)
    sleep(1)
    try:
        driver.execute_script("""document.querySelectorAll('[class="ButtonCaptionText"]')[0].click()""")
    except:
        print('não foi necessário realizar o click-login')
    
    sleep(5)
    
    # TODO garantir que altera para cada index_rpa
    verification_code = Email_API.get_Verification_Code_RMV(INDEX) # index_rpa
    
    driver.find_element(By.CSS_SELECTOR,'[type="text"]').send_keys(verification_code,Keys.ENTER)
    print('inseri o verification code e cliquei no ENTER')
    
    # TODO trocar a forma de avaliar se o verification code deu certo mesmo

    url = r'https://atlas-myrmv.massdot.state.ma.us/eservices/_/#2'
    print(url)
    
    t_wait = 0

    while url == r'https://atlas-myrmv.massdot.state.ma.us/eservices/_/#2':
        sleep(1)
        driver.execute_script("document.querySelectorAll('span').forEach((e)=>{if(e.innerText == 'Search for a Vehicle'){e.click()}})")
        print('cliquei no Search Vehicles')
        url = driver.current_url
        t_wait += 1
        if t_wait == 3:
            sleep(1)
            verification_code = Email_API.get_Verification_Code_RMV(INDEX) # index_rpa
            driver.find_element(By.CSS_SELECTOR,'[type="text"]').send_keys(verification_code,Keys.ENTER)
            print('inseri o verification code e cliquei no ENTER')
            sleep(2)
    
    driver_list.append(driver)
    print(f'\nPARÂMETROS FINAIS:\ndriver_list:{driver_list}\nindex_rpa:{index_rpa}\nn:{n}')
    
    return f'WEBDRIVER CRIADO'


########################################



processing = []
fila = []

@app.post('/rmv')
def rmv(request: VIN):
    print('fui chamado para buscar um VIN')
    
    global n
    global processing
    global driver_list
    global index_rpa
    
    
    bot = automation.BOT().run_rmv
    
    if len(processing) < index_rpa:
        print(f'\nPARÂMETROS INICIAIS:\ndriver_list:{driver_list}\nindex_rpa:{index_rpa}\nn:{n}')
        t = CustomThread(target=bot,args=[request.vin,driver_list[n]])
        n += 1
        if n == index_rpa:
            n = 0

        processing.append(t.start())
        
        super_json = t.join()
        processing.pop()

        print('\n')
        print(t)
        print('existe ainda o seguinte número de processos: ',len(processing))
        print('\n')

        print(f'\nPARÂMETROS FINAIS:\ndriver_list:{driver_list}\nindex_rpa:{index_rpa}\nn:{n}')

        return super_json
    
    elif len(processing) == index_rpa:
        print(f'\nPARÂMETROS INICIAIS:\ndriver_list:{driver_list}\nindex_rpa:{index_rpa}\nn:{n}')
        global fila

        fila.append(request)
        
        print('AGUARDE ATÉ A FILA ESTAR LIBERADA\n')
        for i in range(600):
            
            time.sleep(1)
            while len(processing) < index_rpa:
                fila.pop(0)
                t = CustomThread(target=bot,args=[request.vin,driver_list[n]])
                n += 1
                if n == index_rpa:
                    n = 0
                processing.append(t.start())
                
                super_json = t.join()
                processing.pop()
                
                print(f'\nPARÂMETROS FINAIS:\ndriver_list:{driver_list}\nindex_rpa:{index_rpa}\nn:{n}')
                
                return super_json
    
    
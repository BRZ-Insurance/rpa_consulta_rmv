from lib2to3.pgen2 import driver
import automation
from collections.abc import Callable, Iterable, Mapping
from typing import Any
import threading
import time
from fastapi import FastAPI

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

###################################
driver_list = []
email_index = 0

class VIN(BaseModel):
    vin: str

# @app.post('/initiate_webdrivers')
def init():
    
    global driver_list
    global email_index
        
    print(f'\nPARÂMETROS INICIAIS:\ndriver_list:{driver_list}')
    ########################################
    ENVIRONMENT = 'SERVER_CHROME'
    ########################################
    match ENVIRONMENT:
        case 'SERVER_CHROME':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_service =  service.ChromiumService(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
            driver = webdriver.Chrome(chrome_options,chrome_service,True)
            print('\nEXECUTEI SERVER_CHROME\n')

        case 'LOCAL_CHROME':
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-dev-shm-usage")
            prefs = {"profile.managed_default_content_settings.images": 2} # desabilita o carregamento de imagens
            chrome_options.add_experimental_option("prefs", prefs)
            driver = webdriver.Chrome(options=chrome_options)

    # Verificar se a classe EMAIL está seguindo a mesma numeração !!!
    if email_index == 0:
        name_rpa = 'rap7'
    if email_index == 1:
        name_rpa = 'pra8'
    if email_index == 2:
        name_rpa = 'pra9'
    if email_index == 3:
        name_rpa = 'arp3'
    if email_index == 4:
        name_rpa = 'par5'
    if email_index == 5:
        name_rpa = 'rap6'
    if email_index == 6:
        name_rpa = 'arp2'
    if email_index == 7:
        name_rpa = 'par4'
    if email_index == 8:
        name_rpa = 'rpa1'
    if email_index == 9:
        name_rpa = 'rpa'

    # email_index += 1

    USERNAME = f'{name_rpa}@brzinsurance.com'
    PASSWORD = 'M!QY7GfBMKhP&Mjr'
    
    driver.get("https://atlas-myrmv.massdot.state.ma.us/eservices/_/")
    print('\n',driver.current_url)
    sleep(1)

    Z = 0
    while Z < 20:
        try:
            driver.find_element(By.CSS_SELECTOR,'[aria-label="Username"]').send_keys(USERNAME)
            driver.find_element(By.CSS_SELECTOR,'[aria-label="Password"]').send_keys(PASSWORD,Keys.ENTER)
            sleep(1)
            Z = 20
        except:
            sleep(1)
            print('fazendo login')
            Z += 1
    try:
        driver.execute_script("""document.querySelectorAll('[class="ButtonCaptionText"]')[0].click()""")
    except:
        print('não foi necessário realizar o click-login')
    
    sleep(5)
    
    verification_code = Email_API.get_Verification_Code_RMV(name_rpa)
    
    print(verification_code)

    Z = 0
    while Z == 0:
        try:
            driver.find_element(By.CSS_SELECTOR,'[type="text"]').send_keys(verification_code,Keys.ENTER)
            print('inseri o verification code e cliquei no ENTER')
            Z = 1
        except:
            sleep(5)
            verification_code = Email_API.get_Verification_Code_RMV(name_rpa)
            print('código não inserido')
    
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
            verification_code = Email_API.get_Verification_Code_RMV(name_rpa)
            driver.find_element(By.CSS_SELECTOR,'[type="text"]').send_keys(verification_code,Keys.ENTER)
            print('inseri o verification code e cliquei no ENTER')
            sleep(2)
    
    running = 0
    driver_list.append([driver,running])
    print(url)
    print(f'\nPARÂMETROS FINAIS:\ndriver_list:{driver_list}')
    
    return f'WEBDRIVER CRIADO'

### Caso uma instância do Webdriver é fechada, ainda assim o driver_list continua considerando a existência da instência 


########################################

for i in range(3):
    time.sleep(15)
    init()
    email_index += 1

processing = []
fila = []

@app.post('/rmv')
def rmv(request: VIN):
    
    print('fui chamado para buscar um VIN')
    global processing
    global driver_list
    
    if len(driver_list) < 3:
        global email_index
        init()
        email_index += 1
        if email_index == 10:
            email_index = 0
    
    bot = automation.BOT().run_rmv
    
    if len(processing) < len(driver_list):
        # print(f'\nPARÂMETROS INICIAIS:\ndriver_list:{driver_list}')

        for DRIVER in driver_list:
            print(DRIVER[0])
            print(DRIVER[1])

            if DRIVER[1] == 0:
                DRIVER[1] = 1
                try: # existe a possibilidadte da instância ter desconectado com o DevTools. Por isso, é necessário tirar a instância da lista e criar outra no local
                    t = CustomThread(target=bot,args=[request.vin,DRIVER[0]])
                    processing.append(t.start())
                    super_json = {}
                    super_json = t.join()
                    if super_json == 'X':
                        driver_list.remove(DRIVER)
                        init()
                        email_index += 1
                except:
                    driver_list.remove(DRIVER)
                processing.pop()
                DRIVER[1] = 0
                break
        
            

        

        # print(f'\nPARÂMETROS FINAIS:\ndriver_list:{driver_list}')

        return super_json
    
    elif len(processing) >= len(driver_list):
        print(f'\nPARÂMETROS INICIAIS:\ndriver_list:{driver_list}')
        global fila

        fila.append(request)
        
        print('AGUARDE ATÉ A FILA ESTAR LIBERADA\n')
        for i in range(30):
            print('ESPERANDO DRIVER PARA EXECUTAR')
            time.sleep(2)
            while len(processing) < len(driver_list):
                req = fila.pop(0)
                
                for DRIVER in driver_list:
                    print(DRIVER[0])
                    print(DRIVER[1])
                    if DRIVER[1] == 0:
                        DRIVER[1] = 1
                        t = CustomThread(target=bot,args=[request.vin,DRIVER[0]])
                        processing.append(t.start())
                        super_json = t.join()
                        processing.pop()
                        DRIVER[1] = 0
                        break
                        
                super_json = t.join()
                
                
                print(f'\nPARÂMETROS FINAIS:\ndriver_list:{driver_list}')
                
                return super_json
    
    
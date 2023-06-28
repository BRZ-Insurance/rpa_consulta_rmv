from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chromium import service
from time import sleep
import os
import Email_API


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
            prefs = {"profile.managed_default_content_settings.images": 2} # desabilita o carregamento de imagens
            chrome_options.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Chrome(options=chrome_options)
    
    def run_carrier(self,url):

        self.driver.get(url)
        print(self.driver.current_url)
        return self.driver

    def run_rmv(self,vin):
        USERNAME = 'rpa1@brzinsurance.com'
        PASSWORD = 'M!QY7GfBMKhP&Mjr'

        driver = self.driver
        while True:
            try:
                driver.get("https://atlas-myrmv.massdot.state.ma.us/eservices/_/")
                print(vin)
                print(self.driver.current_url)
                sleep(2)
                driver.find_element(By.CSS_SELECTOR,'[aria-label="Username"]').send_keys(USERNAME)
                driver.find_element(By.CSS_SELECTOR,'[aria-label="Password"]').send_keys(PASSWORD, Keys.ENTER)
                sleep(6)
                verification_code = Email_API.get_Verification_Code_RMV(1) # index_rpa
                print(verification_code)
                driver.find_element(By.CSS_SELECTOR,'[type="text"]').send_keys(verification_code,Keys.ENTER)
                print('inseri o verification code e cliquei no ENTER')
                sleep(3)
                while True:
                    driver.execute_script("document.querySelectorAll('span').forEach((e)=>{if(e.innerText == 'Search for a Vehicle'){e.click()}})")
                    print('cliquei no Search Vehicles')
                    sleep(3)
                    break
                break
            except:
                print('nova tentativa')
                sleep(9)

        while True:
            try:
                try:
                    driver.execute_script("""
                        document.querySelectorAll('a').forEach(
                            (e)=>{if(e.textContent == 'Go back to Search Vehicles'){
                                e.click()
                            }}
                        )
                    """)
                except:
                    pass

                sleep(0.1)
                driver.find_element(By.CSS_SELECTOR,"#Dd-6").clear()
                sleep(0.1)
                driver.find_element(By.CSS_SELECTOR,"#Dd-6").send_keys(vin)
                
                sleep(2)
                driver.execute_script("""
                    document.querySelectorAll('[class="ButtonCaptionText"]').forEach(
                        (e)=>{if(e.innerText == "Search"){e.click()}}
                    )
                """)

                sleep(2)
                primary_owner = driver.execute_script("""
                    primary_owner = ''
                    document.querySelectorAll('span').forEach(
                        (e)=>{if(e.innerText == 'Primary Owner\\n:'){
                            primary_owner = e.nextElementSibling.innerText
                        }}
                    )
                    return primary_owner
                """)

                
                driver.find_element(By.CSS_SELECTOR,'[style=" font-weight:bold;  color: #1a0dae;  font-size: 12pt; "]').click()

                ### Vehicle Ownership Table ###
                try:
                    sleep(3)
                    vehicle_ownership = driver.execute_script("""
                        A = []
                        document.querySelectorAll('[class="DocTableBody"]')[0]?.querySelectorAll('tr').forEach(
                            (r)=>{
                                A.push(r.querySelectorAll('td')[2]?.innerText)
                            }
                        )
                        return A
                    """)
                except Exception as e:
                    
                    print('Erro ao captar Vehicle Ownership Table')
                    driver.find_element(By.CSS_SELECTOR,'[id="ManagerBackNavigation"]').click()
                    return
                
                try:
                    dados_ownership = {"vehicle_year_make_model":vehicle_ownership[0],"vehicle_identification_number":vehicle_ownership[1],"mailing_address":vehicle_ownership[2].strip()}
                except:
                    dados_ownership = {}
                    
                ### Registration Table ###
                try:
                    registration = driver.execute_script("""
                        B = []
                        document.querySelectorAll('[class="DocTableBody"]')[1]?.querySelectorAll('tr').forEach(
                            (r)=>{
                                B.push(r.querySelectorAll('td')[2]?.innerText)
                            }
                        )
                        return B
                    """)
                    if len(registration) == 7:
                        dados_registration = {"title":registration[0],"plate_number":registration[1],"plate_type":registration[2],"registration":registration[3],"registration_expires":registration[4],"title_status":registration[5],"registration_status":registration[6]}
                    if len(registration) == 6:
                        dados_registration = {"title":registration[0],"plate_number":registration[1],"plate_type":registration[2],"title_status":registration[3],"registration_status":registration[4],"registration_cancelled":registration[5]}
                    if len(registration) == 3:
                        dados_registration = {"title":registration[0],"title_status":registration[1],"registration_status":registration[2]}
                except Exception as e:
                    
                    print('Erro ao captar Registration Table')
                    driver.find_element(By.CSS_SELECTOR,'[id="ManagerBackNavigation"]').click()
                    return
                
                ## Recuperar propriedades do veiculo ###
                try:
                    driver.find_elements(By.CSS_SELECTOR,'[class="DocTabText"]')[8].click()
                    sleep(1)
                    vehicle_details = driver.execute_script("""
                        C = []
                        document.querySelectorAll('[id="Dh-b"] [class="DocTableBody"] tr').forEach(
                            (r)=>{
                                C.push(r.querySelectorAll('td')[2]?.innerText)
                            }
                        )
                        return C
                    """)
                    dados_vehicle = {"year":vehicle_details[0],"make":vehicle_details[1],"model":vehicle_details[2],"color":vehicle_details[3],"vin":vehicle_details[4]}
                except Exception as e:
                    
                    print('Erro ao Recuperar propriedades do veiculo')
                    driver.find_element(By.CSS_SELECTOR,'[id="ManagerBackNavigation"]').click()
                    return
                
                ### Odometer ###
                try:
                    #self.encontrar_elemento(driver,'[class="DocTabText"]',"btn-odometer",9,click=True)
                    driver.execute_script('document.querySelectorAll("span").forEach((e)=>{if(e.innerText == "Odometer"){e.click()}})')
                    sleep(2)
                    odometer = driver.find_element(By.CSS_SELECTOR,'[aria-label="Odometer"] tbody td').text # etapa 26
                    dados_odometer = {"odometer":odometer}
                except Exception as e:
                    
                    print('Erro ao captar Odometer')
                    driver.find_element(By.CSS_SELECTOR,'[id="ManagerBackNavigation"]').click()
                    return
                
                ### Insurance ###
                try:
                    driver.execute_script('document.querySelectorAll("span").forEach((e)=>{if(e.innerText == "Insurance"){e.click()}})')
                    sleep(2)
                    insurance = driver.execute_script("""
                        D = []
                        i = {}
                        document.querySelectorAll('[aria-label="Insurance Policies"]').forEach(
                            (t)=>{
                                t.querySelectorAll('thead th').forEach(
                                    (e)=>{
                                        i[e.innerText.toUpperCase()] = ''
                                        
                                    })
                                if(t.querySelectorAll('tr')[1].querySelectorAll('td').length == 12 ){
                                t.querySelectorAll('tr')[1].querySelectorAll('td').forEach(
                                    (e)=>{
                                        D.push(e.innerText.toUpperCase())  
                                    })
                                }
                            }
                        )
                        return D
                    """)
                    if len(insurance) == 0:
                        dados_insurance = {"policy":"No Policy","policy_holder":"No Policy_holder","term_effective":"","term_expire":""}
                    else:
                        dados_insurance = {"policy":insurance[0],"policy_holder":insurance[1],"term_effective":insurance[4],"term_expire":insurance[5]}
                except Exception as e:
                    
                    print('Erro ao captar Insurance')
                    driver.find_element(By.CSS_SELECTOR,'[id="ManagerBackNavigation"]').click()
                    return
                
                ### Obligations ###
                try:
                    driver.execute_script('document.querySelectorAll("span").forEach((e)=>{if(e.innerText == "Obligations"){e.click()}})')
                    sleep(2)
                    trs = driver.find_elements(By.CSS_SELECTOR,'[class="DocTableBody"]')[3].find_elements(By.TAG_NAME,'tr')
                    obligations = []
                    for tr in trs:
                        ticket_number = tr.find_elements(By.TAG_NAME,'td')[0].text
                        if ticket_number == 'No rows returned.':
                            break
                        type = tr.find_elements(By.TAG_NAME,'td')[1].text
                        recorded_year = tr.find_elements(By.TAG_NAME,'td')[2].text
                        cease = tr.find_elements(By.TAG_NAME,'td')[5].text
                        obligations.append({"ticket_number":ticket_number,"type":type,"recorded_year":recorded_year,"cease":cease})
                except Exception as e:
                    
                    print('Erro ao captar Obligations')
                    driver.find_element(By.CSS_SELECTOR,'[id="ManagerBackNavigation"]').click()
                    return 

                print('Executou etapa:  Final')
                
                super_json = {"primary_owner":primary_owner,"ownership":dados_ownership,"registration":dados_registration,"vehicle":dados_vehicle,"insurance":dados_insurance,"odometer":dados_odometer,"obligations":obligations,"status":"Conclude"}

                if super_json:
                    return super_json
                
                break                 
            except Exception as error:
                print('nova tentativa\n')
                print(error)
                sleep(3)
                
            
        print(super_json)

        return self.driver
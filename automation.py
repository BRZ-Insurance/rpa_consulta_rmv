from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chromium import service
from time import sleep
import os
import Email_API


class BOT():
    def __init__(self) -> None:
        
        # n = 0
        # while n < 10:
        #     try:
        #         # Fazer algo
        #         n = 10
        #     except:
        #         sleep(1)
        #         print('alguma coisa')
        
        pass
    
    def run_carrier(self,url):

        self.driver.get(url)
        print(self.driver.current_url)
        return self.driver

    def run_rmv(self,vin,driver: webdriver.Chrome):

        if len(driver.find_elements(By.CSS_SELECTOR,'[type="password"]')) == 1:
            PASSWORD = 'M!QY7GfBMKhP&Mjr'
            driver.find_elements(By.CSS_SELECTOR,'[type="password"]')[0].send_keys(PASSWORD,Keys.ENTER)
        
        if len(driver.find_elements(By.CSS_SELECTOR,'[class="IconCaptionText"]')) == 7:
            driver.find_elements(By.CSS_SELECTOR,'[class="IconCaptionText"]')[4].click()
            sleep(2)

        J = {"vin/plate":vin,"url":driver.current_url}
        driver.find_element(By.CSS_SELECTOR,'[id="Dd-6"]').clear()
        sleep(0.2)
        driver.find_element(By.CSS_SELECTOR,'[id="Dd-6"]').send_keys(vin,Keys.ENTER)
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
        try:
            driver.find_elements(By.CSS_SELECTOR,'span')[6].click()
        except:
            driver.execute_script("""
                document.querySelectorAll('span')[6].click()
            """)
        

        n = 0
        while n < 10:
            try:
                driver.find_elements(By.CSS_SELECTOR,'[class="DocTabText"]')[7].click()
                sleep(1)
                J['liens'] = driver.find_elements(By.CSS_SELECTOR,'[class="DocTableBody"]')[3].find_element(By.CSS_SELECTOR,'tr').text
                liens = driver.find_elements(By.CSS_SELECTOR,'[class="DocTableBody"]')[3].find_element(By.CSS_SELECTOR,'tr').text
                n = 10
            except:
                sleep(0.2)
                print('tentando clicar na aba LIENS')

        n = 0
        while n < 10:
            try:
                driver.find_elements(By.CSS_SELECTOR,'[class="DocTabText"]')[8].click()
                sleep(1)
                J['vehicle_details_1'] = driver.find_elements(By.CSS_SELECTOR,'[class="DocTableBody"]')[3].text
                J['vehicle_details_2'] = driver.find_elements(By.CSS_SELECTOR,'[class="DocTableBody"]')[4].text
                n = 10
                vehicle_details = driver.execute_script("""
                    C = []
                    document.querySelectorAll('[id="Dh-b"] [class="DocTableBody"] tr').forEach(
                        (r)=>{
                            C.push(r.querySelectorAll('td')[2].innerText)
                        }
                    )
                    return C
                """)
                dados_vehicle = {"year":vehicle_details[0],"make":vehicle_details[1],"model":vehicle_details[2],"color":vehicle_details[3],"vin":vehicle_details[4]}
            except:
                sleep(0.2)
                print('tentando clicar na aba VEHICLE DETAIL')
                n += 1
        
        n = 0
        while n < 10:
            try:
                # driver.find_elements(By.CSS_SELECTOR,'[class="DocTabText"]')[9].click()
                driver.execute_script("""
                    document.querySelectorAll('span').forEach(
                    (e)=>{if(e.innerText == 'Odometer'){e.click()}}
                )""")
                sleep(1)
                J['odometer'] = driver.find_elements(By.CSS_SELECTOR,'[class="DocTableBody"]')[3].text
                if J['odometer'] == None:
                    J['odometer'] = driver.execute_script("""
                        return document.querySelectorAll('[data-row="1"]')[3].innerText
                    """)
                n = 10
                odometer = driver.find_element(By.CSS_SELECTOR,'[aria-label="Odometer"] tbody td').text # etapa 26
                dados_odometer = {"odometer":odometer}
            except:
                sleep(0.2)
                print('tentando clicar na aba ODOMETER')
                n += 1

        n = 0
        while n < 10:
            try:
                driver.find_elements(By.CSS_SELECTOR,'[class="DocTabText"]')[3].click()
                sleep(1)
                J['obligations'] = driver.find_elements(By.CSS_SELECTOR,'[class="DocTableBody"]')[3].text
                n = 10

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

            except:
                sleep(0.2)
                print('tentando clicar na aba OBLIGATIONS')
                n += 1


        n = 0
        while n < 10:
            try:
                driver.find_elements(By.CSS_SELECTOR,'[class="DocTabText"]')[5].click()
                sleep(1)
                J['insurance'] = driver.find_elements(By.CSS_SELECTOR,'[class="DocTableBody"]')[4].text
                n = 10

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
                    dados_insurance = {}
                else:
                    dados_insurance = {"policy":insurance[0],"policy_holder":insurance[1],"term_effective":insurance[4],"term_expire":insurance[5]}
            except:
                sleep(0.2)
                print('tentando clicar na aba INSURANCE')
                n += 1
        
        n = 0
        while n < 10:
            try:
                trs = driver.find_elements(By.CSS_SELECTOR,'[class="DocTableBody"]')[0].find_elements(By.CSS_SELECTOR,'tr')
                for tr in trs:
                    key = tr.find_elements(By.CSS_SELECTOR,'td')[0].text
                    value = tr.find_elements(By.CSS_SELECTOR,'td')[2].text
                    J[key] = value
                n = 10

                vehicle_ownership = driver.execute_script("""
                    A = []
                    document.querySelectorAll('[class="DocTableBody"]')[0].querySelectorAll('tr').forEach(
                        (r)=>{
                            A.push(r.querySelectorAll('td')[2].innerText)
                        }
                    )
                    return A
                """)
                dados_ownership = {"vehicle_year_make_model":vehicle_ownership[0],"vehicle_identification_number":vehicle_ownership[1],"mailing_address":vehicle_ownership[2]}

            except:
                sleep(0.2)
                print('tentando ler as TABELAS PRINCIPAIS - VEHICLE OWNERSHIP')
                n += 1

        n = 0
        while n < 10:
            try:
                trs = driver.find_elements(By.CSS_SELECTOR,'[class="DocTableBody"]')[1].find_elements(By.CSS_SELECTOR,'tr')
                for tr in trs:
                    key = tr.find_elements(By.CSS_SELECTOR,'td')[0].text
                    value = tr.find_elements(By.CSS_SELECTOR,'td')[2].text
                    J[key] = value
                n = 10

                m = 0
                while m < 5:
                    registration = driver.execute_script("""
                        B = []
                        document.querySelectorAll('[class="DocTableBody"]')[1].querySelectorAll('tr').forEach(
                            (r)=>{
                                B.push(r.querySelectorAll('td')[2].innerText)
                            }
                        )
                        return B
                    """)

                    if len(registration) == 8:
                        dados_registration = {"title":registration[0],"plate_number":registration[1],"plate_type":registration[2],"registration":registration[3],"registered_weight":registration[4],"registration_expires":registration[5],"title_status":registration[6],"registration_status":registration[7]}
                        m = 5
                    elif len(registration) == 7:
                        dados_registration = {"title":registration[0],"plate_number":registration[1],"plate_type":registration[2],"registration":registration[3],"registration_expires":registration[4],"title_status":registration[5],"registration_status":registration[6]}
                        m = 5
                    elif len(registration) == 6:
                        dados_registration = {"title":registration[0],"plate_number":registration[1],"plate_type":registration[2],"title_status":registration[3],"registration_status":registration[4],"registration_cancelled":registration[5]}
                        m = 5
                    elif len(registration) == 3:
                        dados_registration = {"title":registration[0],"title_status":registration[1],"registration_status":registration[2]}
                        m = 5
                    else:
                        dados_registration = {}
                        m += 1
                        sleep(0.2)

            except:
                sleep(0.2)
                print('tentando ler as TABELAS PRINCIPAIS - REGISTRATION')
                n += 1
        
        n = 0
        while n < 10:
            try:
                driver.find_element(By.CSS_SELECTOR,'[id="ManagerBackNavigation"]').click()
                n = 10
            except:
                sleep(0.2)
                print('tentando clicar na volta para a tela de SEARCH')
                n += 1
        
        super_json = {"primary_owner":primary_owner,"ownership":dados_ownership,"liens":liens,"registration":dados_registration,"vehicle":dados_vehicle,"insurance":dados_insurance,"odometer":dados_odometer,"obligations":obligations,"status":"Conclude"}
        return super_json
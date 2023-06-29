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

        J = {"vin":vin,"url":driver.current_url}
        driver.find_element(By.CSS_SELECTOR,'[id="Dd-6"]').clear()
        sleep(0.2)
        driver.find_element(By.CSS_SELECTOR,'[id="Dd-6"]').send_keys(vin,Keys.ENTER)
        sleep(1)
        driver.find_elements(By.CSS_SELECTOR,'span')[6].click()
        

        n = 0
        while n < 10:
            try:
                driver.find_elements(By.CSS_SELECTOR,'[class="DocTabText"]')[7].click()
                sleep(1)
                J['liens'] = driver.find_elements(By.CSS_SELECTOR,'[class="DocTableBody"]')[3].find_element(By.CSS_SELECTOR,'tr').text
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

        return J
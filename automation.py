from selenium import webdriver
from selenium.webdriver.common.by import By
from search_element import SearchElement

class BOT():
    def __init__(self) -> None:
        ### Options ###
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        prefs = {"profile.managed_default_content_settings.images":2}
        options.add_experimental_option("prefs", prefs)

        ### Instance ChromeDriver ###
        self.driver = webdriver.Chrome(options=options)
        search = SearchElement(self.driver)

    def open_page(self,page):
        """Método que faz o bot abrir uma página"""
        self.driver.get(page)

           



        

        
    


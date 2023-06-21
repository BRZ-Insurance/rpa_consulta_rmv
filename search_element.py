from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import webdriver_manager

class SearchElement():
    def __init__(self,driver: webdriver.Chrome) -> None:
        self.driver = driver

    def content(self,css_selector: str):
        """Utilize um css_selector para buscar o innerText do elemento"""
        content = None
        while content == None:
            try:
                content = self.driver.execute_script(f"""
                    R = document.querySelectorAll('{css_selector}')[0]?.innerText
                    return R;
                """)
                if content != None:
                    return content
                else:
                    pass
            except:
                pass

            try:
                content = self.driver.execute_script(f"""
                    R = document.querySelectorAll({css_selector})[0]?.innerText
                    return R;
                """)
                if content != None:
                    return content
                else:
                    pass
            except:
                pass

            try:
                content = self.driver.execute_script(f"""
                    R = document.querySelectorAll("{css_selector}")[0]?.innerText
                    return R;
                """)
                if content != None:
                    return content
                else:
                    pass
            except:
                pass

            try:
                content = self.driver.execute_script(f"""
                    R = document.querySelectorAll({css_selector})[0]?.textContent
                    return R;
                """)
                if content != None:
                    return content
                else:
                    pass
            except:
                pass

            try:
                content = self.driver.execute_script(f"""
                    R = document.querySelectorAll({css_selector})[0]?.innerHTML
                    return R;
                """)
                if content != None:
                    return content
                else:
                    pass
            except:
                pass

            try:
                content = self.driver.execute_script(f"""
                    R = document.querySelectorAll("{css_selector}")[0]?.getAttribute('value')
                    return R;
                """)
                if content != None:
                    return content
                else:
                    pass
            except:
                pass
            
            try:
                content = self.driver.execute_script(f"""
                    R = document.querySelectorAll("{css_selector}")[0]?.nextElementSibling.innerText
                    return R;
                """)
                if content != None:
                    return content
                else:
                    pass
            except:
                pass

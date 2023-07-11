# Proj.Selenium_Server
projeto de automação_selenium para execução do servidor (Heroku)

from selenium.webdriver import Remote

driver = Remote(desired_capabilities={'browserName':'chrome'})
driver.get('https://atlas-myrmv.massdot.state.ma.us/eservices/_/#3')
driver.save_screenshot('loginRMV.png')


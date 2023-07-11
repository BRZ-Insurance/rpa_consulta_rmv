from selenium import webdriver
from fastapi import FastAPI

app = FastAPI()

@app.post('/rmv')
def rmv():
    driver = webdriver.Firefox()
    driver.get('https://atlas-myrmv.massdot.state.ma.us/eservices/_/')
    X = driver.page_source
    return X
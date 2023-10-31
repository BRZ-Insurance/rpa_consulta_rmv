from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from selenium import webdriver

app = FastAPI()

class Req(BaseModel):
    policy_id: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/")
async def issue_policy(req: Req):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.set_capability('selenoid:options',{"enableVideo": False, "enableVNC":True})
    chrome_options.add_experimental_option('prefs',{
        "browserName": "chrome",
        "browserVersion": "115.0",
        "selenoid:options": {
            "enableVideo": False,
            "enableVNC":True
        }
    })

    webdriver.Remote(
        command_executor="http://161.35.14.62:4444/wd/hub",
        options=chrome_options
    )
    
    return req

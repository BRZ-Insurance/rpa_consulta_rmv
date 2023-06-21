from fastapi import FastAPI
from fastapi import Request
from pydantic import BaseModel
from automation import BOT


app = FastAPI()

bots_list = []
bot = BOT()

class Body(BaseModel):
    page: str


@app.get('/')
async def run():
    global bot
    bot.open_page('https://www.google.com/')

    
@app.post('/')
async def page(Body: Body):
    print(Body)
    print(Body.page)
    bot.open_page(Body.page)
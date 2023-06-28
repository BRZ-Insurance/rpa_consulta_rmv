import automation
import threading
import time
import fastapi 

app = fastapi.FastAPI()

@app.get('/bot')
def call_bot():
    bot1 = threading.Thread(target=automation.BOT().run,args=["Reik"])
    bot2 = threading.Thread(target=automation.BOT().run,args=["Of"])
    bot3 = threading.Thread(target=automation.BOT().run,args=["Lake"])

    bot1.start()
    bot2.start()
    bot3.start()



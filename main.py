import automation
from collections.abc import Callable, Iterable, Mapping
from typing import Any
import threading
import time
from fastapi import FastAPI, Request
import json

app = FastAPI()

class CustomThread(threading.Thread):
    def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,*self._kwargs)
        
    def join(self):
        threading.Thread.join(self)
        return self._return


#TODO implementar um meio de fazer rodar em ordem

@app.post('/carrier')
async def call_bot(request: Request):
    J = await request.json()

    bot = automation.BOT().run_carrier

    bot_runner = threading.Thread(target=bot,args=[J.get('url')])
    
    bot_runner.start()
    
    bot_runner.join()

    return 'executado'

@app.post('/rmv')
async def call_bot(request: Request):
    J = await request.json()

    bot = automation.BOT().run_rmv

    # bot_runner = threading.Thread(target=bot,args=[J.get('vin')])
    bot_runner = CustomThread(target=bot,args=[J.get('vin')])

    bot_runner.start()    
    
    super_json = bot_runner.join()

    return super_json
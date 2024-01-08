import _thread
import json

import uvicorn
from fastapi import FastAPI
import API.test_request

app = FastAPI()
app.mount("/", test_request.api)

port = 8000


def start(args):

    print('starting HTTP server (API) \t', 'config.json parsing')
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        raise Exception("ERROR: config.json not found!")

    try:
        global port
        port = config['http_port']
    except Exception as e:
        raise Exception("ERROR: config.json : data is not valid", e)

    print('starting HTTP server (API) \t', 'starting uvicorn')
    _thread.start_new_thread(api_thread, ())


def api_thread():
    uvicorn.run("API:app", host='127.0.0.1', port=port, reload=False)
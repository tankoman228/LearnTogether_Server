import _thread
import json

import uvicorn
from fastapi import FastAPI
import API.test_request
import API.forum
from API import register_auth

app = FastAPI()
app.mount("/test/", test_request.api)
app.mount("/login/", register_auth.api)
app.mount("/", API.forum.app)

port = 8000
ip = ''
host = ''


def start(args):

    print('starting HTTP server (API) \t', 'config.json parsing')
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        raise Exception("ERROR: config.json not found!")

    try:
        global port, host
        port = config['http_port']
        host = config['host']
    except Exception as e:
        raise Exception("ERROR: config.json : data is not valid", e)

    print('starting HTTP server (API) \t', 'starting uvicorn')
    _thread.start_new_thread(api_thread, ())


def api_thread():
    uvicorn.run("API:app", host=host, port=port, reload=False)

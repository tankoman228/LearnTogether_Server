from fastapi import FastAPI

api = FastAPI()


@api.post('/Test')
def index():
    return {"Success": True}

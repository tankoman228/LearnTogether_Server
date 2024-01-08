from fastapi import FastAPI

api = FastAPI()


@api.get('/Test')
def index():
    return {"Hello": "TestApt$ \n\n\n\n"}

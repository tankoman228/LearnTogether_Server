from fastapi import FastAPI, Body

app = FastAPI()


@app.post('/get_infos')
def fef(payload: dict = Body(...)):
    pass


@app.post('/download')
def fef(payload: dict = Body(...)):
    pass


@app.post('/add_info')
def fef(payload: dict = Body(...)):
    pass

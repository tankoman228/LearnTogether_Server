from fastapi import FastAPI, Body

app = FastAPI()


@app.post('get_news')
def fef(payload: dict = Body(...)):
    pass


@app.post('accept_news')
def fef(payload: dict = Body(...)):
    pass


@app.post('add_news')
def fef(payload: dict = Body(...)):
    pass


@app.post('add_task')
def fef(payload: dict = Body(...)):
    pass


@app.post('add_vote')
def fef(payload: dict = Body(...)):
    pass


@app.post('vote')
def fef(payload: dict = Body(...)):
    pass


@app.post('update_task_status')
def wenomechainsama(payload: dict = Body(...)):
    pass

from fastapi import FastAPI, Body

app = FastAPI()


@app.post('/create_token')
def fef(payload: dict = Body(...)):
    pass


@app.post('/delete_ib')
def fef(payload: dict = Body(...)):
    pass


@app.post('/change_user_role')
def fef(payload: dict = Body(...)):
    pass


@app.post('/new_role')
def fef(payload: dict = Body(...)):
    pass


@app.post('/edit_role')
def fef(payload: dict = Body(...)):
    pass


@app.post('/delete_role')
def fef(payload: dict = Body(...)):
    pass


@app.post('/delete_account')
def fef(payload: dict = Body(...)):
    pass


@app.post('/block_account')
def fef(payload: dict = Body(...)):
    pass


@app.post('/complaint')
def fef(payload: dict = Body(...)):
    pass


@app.post('/get_complaints')
def fef(payload: dict = Body(...)):
    pass

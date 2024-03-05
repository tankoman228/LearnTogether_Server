from fastapi import FastAPI, Body

app = FastAPI()


@app.post('accept_ib')
def fef(payload: dict = Body(...)):
    pass


@app.post('delete_ib')
def fef(payload: dict = Body(...)):
    pass


@app.post('change_user_role')
def fef(payload: dict = Body(...)):
    pass


@app.post('new_role')
def fef(payload: dict = Body(...)):
    pass


@app.post('edit_role')
def fef(payload: dict = Body(...)):
    pass

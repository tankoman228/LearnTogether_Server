from fastapi import FastAPI, Body

app = FastAPI()


@app.post('get_meetings')
def fef(payload: dict = Body(...)):
    pass


@app.post('join_meeting')
def fef(payload: dict = Body(...)):
    pass


@app.post('update_meeting_join_status')
def fef(payload: dict = Body(...)):
    pass

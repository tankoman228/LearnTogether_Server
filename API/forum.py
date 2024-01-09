from fastapi import FastAPI, Body
from sqlalchemy import DateTime
from sqlalchemy import or_

import DB
from API import AuthSession

app = FastAPI()


@app.get('/get_asks')
def sdc(payload: dict = Body(...)):

    if str(payload['session_token']) not in AuthSession.auth_sessions.keys():
        return {"Error": 'Unregistered'}

    group = int(payload['group'])
    search_str = payload['search_string']
    before_time = DateTime(payload['before_time'])
    number = int(payload['number'])

    asks = DB.Ses.query(DB.ForumAsk).join(DB.InfoBase).filter(
        DB.InfoBase.ID_Group == group and DB.InfoBase.WhenAdd >= before_time).all()

    search_words = search_str.split()
    search_conditions = []
    for word in search_words:
        # Ищем вопросы, у которых заголовок или тег содержит искомое слово
        search_conditions.append(DB.InfoBase.Title.ilike(f"%{word}%"))
        search_conditions.append(DB.InfoTag.tag.Text.ilike(f"%{word}%"))

    # Формируем итоговый запрос, который учитывает все условия поиска
    result = []
    i = 1
    for ask in asks:
        # Если вопрос соответствует хотя бы одному условию поиска, добавляем его в результат
        if any(DB.Ses.query(DB.InfoBase).join(DB.InfoTag).filter(
                DB.InfoBase.ID_InfoBase == int(ask.ID_InfoBase), or_(*search_conditions)).all()):
            result.append({
                "title": ask.infobase.Title,
                "datetime": ask.infobase.WhenAdd,
                "text": ask.infobase.Text,
                "solved": ask.Solved
            })
            i += 1
            if i > number:
                return

    return {"Asks": result}


@app.post('/add_forum_ask')
def dsd(payload: dict = Body(...)):

    session = AuthSession.auth_sessions[payload['session_token']]

    id_group = payload["id_group"]
    title = payload["title"]
    text = payload["text"]
    tags = payload["tags"].replace(' ', '').split(',')



@app.post('/mark_solved')
def dsds(payload: dict = Body(...)):
    pass


@app.post('/delete_ask')
def dsds(payload: dict = Body(...)):
    pass


@app.post('/')
def dsds(payload: dict = Body(...)):
    pass

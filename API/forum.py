import datetime

from fastapi import FastAPI, Body
from sqlalchemy import DateTime

import DB
from API import AuthSession

app = FastAPI()


@app.post('/get_asks')
def sdc(payload: dict = Body(...)):
    if str(payload['session_token']) not in AuthSession.auth_sessions.keys():
        return {"Error": 'Unregistered'}

    group = int(payload['group'])
    search_str = payload['search_string']
    number = int(payload['number'])

    try:
        before_time = DateTime(payload['before_time'])
    except:
        before_time = datetime.datetime.utcnow

    asks = DB.Ses.query(DB.ForumAsk).join(DB.InfoBase).where(
        DB.InfoBase.ID_Group == group and DB.InfoBase.WhenAdd <= before_time).order_by(DB.InfoBase.WhenAdd.desc()).all()

    result = []
    found = 0

    for ask in asks:

        if found >= number:
            break

        if search_str in ask.infobase.Title:
            result.append({
                "title": ask.infobase.Title,
                "datetime": ask.infobase.WhenAdd,
                "text": ask.infobase.Text,
                "solved": ask.Solved
            })
            found += 1
            continue

        for tag in ask.infobase.tags:
            if search_str in tag.tag.Text:
                result.append({
                    "title": ask.infobase.Title,
                    "datetime": ask.infobase.WhenAdd,
                    "text": ask.infobase.Text,
                    "solved": ask.Solved
                })
                found += 1
                break

    return {"Asks": result}


@app.post('/add_forum_ask')
def ask_adder(payload: dict = Body(...)):
    try:
        session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

        id_group = payload["id_group"]
        title = payload["title"]
        text = payload["text"]
        tags = payload["tags"].replace(' ', '').split(',')

        tags_id = []

        if not session.allowed("forum_allowed", id_group):
            return {"Error": "Forbidden"}

        for tag in tags:
            db_tag = DB.Ses.query(DB.Tag).where(str(tag) == DB.Tag.Text).first()
            if db_tag:
                tags_id.append(db_tag.ID_Tag)
            else:
                new_tag = DB.Tag(Text=tag)
                DB.Ses.add(new_tag)
                DB.Ses.commit()

                tags_id.append(new_tag.ID_Tag)

        ib = DB.InfoBase(ID_Group=id_group, ID_Account=session.account.ID_Account, Title=title, Text=text, Type='a')
        DB.Ses.add(ib)
        DB.Ses.commit()

        for tid in tags_id:
            DB.Ses.add(DB.InfoTag(ID_Tag=tid, ID_InfoBase=ib.ID_InfoBase))
            DB.Ses.commit()

        fa = DB.ForumAsk(ID_InfoBase=ib.ID_InfoBase)
        DB.Ses.add(fa)
        DB.Ses.commit()

        return {"Success": "Success!"}

    except Exception as e:
        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}


@app.put('/mark_solved')
def dsds(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    ask = DB.Ses.query(DB.ForumAsk).where(DB.ForumAsk.ID_ForumAsk == int(payload['id_ask'])).first()

    if not ask:
        return {"Error": "Not Found"}

    if (session.allowed("forum_allowed", ask.infobase.ID_Group) and
            ((session.allowed("moderate_publications", ask.infobase.ID_Group) or
              ask.infobase.ID_Account == session.account.ID_Account))):

        try:
            ask.Solved = True
            DB.Ses.commit()
            return {"Success": "Success!"}
        except Exception as e:
            print(e)
            DB.Ses.rollback()
            return {"Error": "DB error"}

    return {"Error": "Not allowed"}


@app.delete('/delete_ask')
def dsds(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    ask = DB.Ses.query(DB.ForumAsk).where(DB.ForumAsk.ID_ForumAsk == int(payload['id_ask'])).first()

    if not ask:
        return {"Error": "Not Found"}

    if (session.allowed("forum_allowed", ask.infobase.ID_Group) and
            ((session.allowed("moderate_publications", ask.infobase.ID_Group) or
              ask.infobase.ID_Account == session.account.ID_Account))):

        try:
            DB.Ses.delete(ask)
            DB.Ses.commit()
            return {"Success": "Success!"}
        except Exception as e:
            print(e)
            DB.Ses.rollback()
            return {"Error": "DB error"}

    return {"Error": "Not allowed"}

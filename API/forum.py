import datetime

from fastapi import FastAPI, Body
from sqlalchemy import DateTime

import DB
from API import AuthSession
from API.Notifications import notificationManager

app = FastAPI()


@app.post('/get_asks')
def sdc(payload: dict = Body(...)):
    if str(payload['session_token']) not in AuthSession.auth_sessions.keys():
        return {"Error": 'Unregistered'}

    group = int(payload['group'])
    search_str = payload['search_string']
    number = int(payload['number'])

    try:
        id_max = int(payload['id_max'])
    except:
        id_max = 99999999999

    asks = (DB.Ses.query(DB.ForumAsk).join(DB.InfoBase).filter(
        DB.InfoBase.ID_Group == group).filter(DB.InfoBase.ID_InfoBase <= id_max).
            order_by(DB.ForumAsk.ID_ForumAsk.desc()).limit(number).all())

    result = []

    for ask in asks:

        if search_str in ask.infobase.Title:
            result.append({
                "Solved": ask.Solved,
                "CommentsFound": len(ask.infobase.comments),
                "AuthorTitle": ask.infobase.account.Title,
                "ID_Author": ask.infobase.ID_Account,
                "ID_InfoBase": ask.ID_InfoBase,
                "ID_ForumAsk": ask.ID_ForumAsk,
                "Rate": ask.infobase.Rate,
                "Text": ask.infobase.Text,
                "Title": ask.infobase.Title,
                "Type": ask.infobase.Type,
                "WhenAdd": str(ask.infobase.WhenAdd)
            })
            continue

        for tag in ask.infobase.tags:
            if search_str in tag.tag.Text:
                result.append({
                    "Solved": ask.Solved,
                    "CommentsFound": len(ask.infobase.comments),
                    "AuthorTitle": ask.infobase,
                    "ID_Author": ask.infobase.ID_Author,
                    "ID_InfoBase": ask.ID_InfoBase,
                    "Rate": ask.infobase.Rate,
                    "Text": ask.infobase.Text,
                    "Title": ask.infobase.Title,
                    "Type": ask.infobase.Type,
                    "WhenAdd": str(ask.infobase.WhenAdd)
                })
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

        notificationManager.send_notifications(ib.ID_Group, 'New asks in the forum!')

        return {"Success": True}

    except Exception as e:
        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}


@app.put('/mark_solved')
def dsds(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    ask = DB.Ses.query(DB.ForumAsk).where(DB.ForumAsk.ID_InfoBase == int(payload['ID_InfoBase'])).first()

    if not ask:
        return {"Error": "Not Found"}

    if (session.allowed("forum_allowed", ask.infobase.ID_Group) and
            ((session.allowed("moderate_publications", ask.infobase.ID_Group) or
              ask.infobase.ID_Account == session.account.ID_Account))):

        try:
            ask.Solved = True
            DB.Ses.commit()

            notificationManager.send_notifications(ask.infobase.ID_Group, 'Question solved: ' + ask.infobase.Title)

            return {"Success": True}
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
            return {"Success": True}
        except Exception as e:
            print(e)
            DB.Ses.rollback()
            return {"Error": "DB error"}

    return {"Error": "Not allowed"}

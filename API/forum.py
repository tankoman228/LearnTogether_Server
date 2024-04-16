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

    db_session = DB.create_session()  # Создание сессии

    try:
        asks = (db_session.query(DB.ForumAsk).join(DB.InfoBase).filter(
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
                        "AuthorTitle": ask.infobase.account.Title,
                        "ID_Author": ask.infobase.ID_Account,
                        "ID_InfoBase": ask.ID_InfoBase,
                        "Rate": ask.infobase.Rate,
                        "Text": ask.infobase.Text,
                        "Title": ask.infobase.Title,
                        "Type": ask.infobase.Type,
                        "WhenAdd": str(ask.infobase.WhenAdd)
                    })
                    break

        return {"Asks": result}

    except Exception as e:
        db_session.rollback()
        db_session.close()
        return {"Error": str(e)}


@app.post('/add_forum_ask')
def ask_adder(payload: dict = Body(...)):
    db_session = DB.create_session()  # Создание сессии

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
            db_tag = db_session.query(DB.Tag).filter(DB.Tag.Text == tag).first()
            if db_tag:
                tags_id.append(db_tag.ID_Tag)
            else:
                new_tag = DB.Tag(Text=tag)
                db_session.add(new_tag)
                db_session.commit()

                tags_id.append(new_tag.ID_Tag)

        ib = DB.InfoBase(ID_Group=id_group, ID_Account=session.account.ID_Account, Title=title, Text=text, Type='a')
        db_session.add(ib)
        db_session.commit()

        for tid in tags_id:
            db_session.add(DB.InfoTag(ID_Tag=tid, ID_InfoBase=ib.ID_InfoBase))
            db_session.commit()

        fa = DB.ForumAsk(ID_InfoBase=ib.ID_InfoBase)
        db_session.add(fa)
        db_session.commit()

        notificationManager.send_notifications(ib.ID_Group, 'New asks in the forum!')

        return {"Success": True}

    except Exception as e:
        print('server error: ', e)
        db_session.rollback()
        db_session.close()
        return {"Error": "Error"}


@app.put('/mark_solved')
def dsds(payload: dict = Body(...)):
    db_session = DB.create_session()  # Создание сессии

    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    ask = db_session.query(DB.ForumAsk).filter(DB.ForumAsk.ID_InfoBase == int(payload['ID_InfoBase'])).first()

    if not ask:
        db_session.close()  # Закрытие сессии
        return {"Error": "Not Found"}

    if (session.allowed("forum_allowed", ask.infobase.ID_Group) and
            ((session.allowed("moderate_publications", ask.infobase.ID_Group) or
              ask.infobase.ID_Account == session.account.ID_Account))):

        try:
            ask.Solved = True
            db_session.commit()

            notificationManager.send_notifications(ask.infobase.ID_Group, 'Question solved: ' + ask.infobase.Title)

            return {"Success": True}
        except Exception as e:
            print(e)
            db_session.rollback()
            db_session.close()
            return {"Error": "DB error"}

    db_session.close()  # Закрытие сессии
    return {"Error": "Not allowed"}


@app.delete('/delete_ask')
def dsds(payload: dict = Body(...)):
    db_session = DB.create_session()  # Создание сессии

    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    ask = db_session.query(DB.ForumAsk).filter(DB.ForumAsk.ID_ForumAsk == int(payload['id_ask'])).first()

    if not ask:
        db_session.close()  # Закрытие сессии
        return {"Error": "Not Found"}

    if (session.allowed("forum_allowed", ask.infobase.ID_Group) and
            ((session.allowed("moderate_publications", ask.infobase.ID_Group) or
              ask.infobase.ID_Account == session.account.ID_Account))):

        try:
            db_session.delete(ask)
            db_session.commit()
            db_session.close()  # Закрытие сессии
            return {"Success": True}
        except Exception as e:
            print(e)
            db_session.rollback()
            db_session.close()  # Закрытие сессии
            return {"Error": "DB error"}

    db_session.close()  # Закрытие сессии
    return {"Error": "Not allowed"}

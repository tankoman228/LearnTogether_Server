from fastapi import FastAPI, Body

import API.AuthSession as AuthSession
from API.Notifications import notificationManager
import DB

api = FastAPI()


@api.post('/get_comments')
def get_comments(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    id_ib = int(payload["id_object"])

    db_session = DB.create_session() # <---------------

    ib = db_session.query(DB.InfoBase).where(DB.InfoBase.ID_InfoBase == id_ib).first()

    if not ib:
        return {"Error": 404}

    if ib.ID_Group not in session.groups_id:
        return {"Error": 403}

    answer = []

    comments = db_session.query(DB.Comment).where(DB.Comment.ID_InfoBase == id_ib).all()
    for comment in comments:
        answer.append({
            "ID_Comment": comment.ID_Comment,
            "ID_Account": comment.ID_Account,
            "Text": comment.Text,
            "Author": comment.account.Title,
            "DateTime": str(comment.WhenAdd),
            "Avatar": comment.account.Icon,
            "Attachment": comment.Attachments
        })

    db_session.close() # <--------------------------

    return {"Comments": answer}


@api.post("/add_comment")
def add_comment(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    db_session = DB.create_session()  # <---------------

    id_ib = int(payload["id_object"])
    ib = db_session.query(DB.InfoBase).where(DB.InfoBase.ID_InfoBase == id_ib).first()

    text = str(payload["text"])
    try:
        attachment = payload["attachment"]
    except:
        attachment = None

    if not ib:
        db_session.close()  # <--------------------------
        return {"Error": 404}

    if ib.Type == 'a':
        if not session.allowed('forum_allowed', ib.ID_Group):
            db_session.close()  # <--------------------------
            return {"Error": 403}
    elif not session.allowed('comments_allowed', ib.ID_Group):
        db_session.close()  # <--------------------------
        return {"Error": 403}

    try:
        new_comment = DB.Comment(ID_InfoBase=id_ib, ID_Account=session.account.ID_Account,
                                 Text=text, Attachments=attachment)

        db_session.add(new_comment)
        db_session.commit()

        notificationManager.send_notification_comment(ib, 'New answer in ' + ib.Title + ': ' + new_comment.Text)

        db_session.close()  # <--------------------------

        return {"Success": True}
    except Exception as e:
        print(e)
        db_session.rollback()
        db_session.close()  # <--------------------------
        return {"Error": "Error"}


@api.post("/delete_comment")
def dgfdregergerged(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    db_session = DB.create_session()  # <---------------

    comment = db_session.query(DB.Comment).where(int(payload['id_comment']) == DB.Comment.ID_Comment).first()

    if not comment:
        db_session.close()  # <--------------------------
        return {"Error": 404}

    if not (session.allowed("moderate_comments", comment.infobase.ID_Group)
            or session.account.ID_Account == comment.ID_Account):
        db_session.close()  # <--------------------------
        return {"Error": 403}

    try:
        db_session.delete(comment)
        db_session.commit()

        db_session.close()  # <--------------------------
        return {"Success": True}

    except Exception as e:
        print(e)
        db_session.rollback()
        db_session.close()  # <--------------------------
        return {"Error": "Not a success"}


@api.post("/rate")
def ppbghrc(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    if not session:
        return {"Error": "Go to 3 happy letters!"}

    rank = int(payload['Rank'])

    if rank not in range(1, 6):
        return {"Error": 412}

    db_session = DB.create_session()  # <---------------
    try:

        rate = (db_session.query(DB.Rank).where
                (DB.Rank.ID_Account == int(session.account.ID_Account) and
                 DB.Rank.ID_InfoBase == int(payload["ID_InfoBase"]))).first()

        if rate:
            db_session.delete(rate)
            db_session.commit()

        rate = DB.Rank(
            ID_InfoBase=payload['ID_InfoBase'],
            ID_Account=session.account.ID_Account,
            Value=rank
        )

        db_session.add(rate)
        db_session.commit()

        ib = db_session.query(DB.InfoBase).where(int(payload['ID_InfoBase']) == DB.InfoBase.ID_InfoBase).first()

        sum = 0.0001
        for i in ib.rates:
            sum += float(i.Value)

        ib.Rate = sum / float(len(ib.rates))

        db_session.commit()

        return {"Success": True}

    except Exception as e:
        print(e)
        db_session.rollback()
        db_session.close()  # <--------------------------
        return {"Error": "500"}

from fastapi import FastAPI, Body

import API.AuthSession as AuthSession
from API.Notifications import notificationManager
import DB

api = FastAPI()


@api.post('/get_comments')
def fkhjkljef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    id_ib = int(payload["id_object"])

    ib = DB.Ses.query(DB.InfoBase).where(DB.InfoBase.ID_InfoBase == id_ib).first()

    if not ib:
        return {"Error": 404}

    if ib.ID_Group not in session.groups_id:
        return {"Error": 403}

    answer = {"comments": []}

    comments = DB.Ses.query(DB.Comment).where(DB.Comment.ID_InfoBase == id_ib).all()
    for comment in comments:
        answer["comments"].append({
            "ID_Comment": comment.ID_Comment,
            "ID_Author": comment.ID_Account,
            "Text": comment.Text,
            "Author": comment.account.Title,
            "DateTime": str(comment.WhenAdd),
            "Avatar": comment.account.Icon,
            "Attachment": comment.Attachments
        })

    return answer


@api.post("/add_comment")
def fefdgbvcf(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    id_ib = int(payload["id_object"])
    ib = DB.Ses.query(DB.InfoBase).where(DB.InfoBase.ID_InfoBase == id_ib).first()

    text = str(payload["text"])
    try:
        attachment = payload["attachment"]
    except:
        attachment = None

    if not ib:
        return {"Error": 404}

    if ib.Type == 'a':
        if not session.allowed('forum_allowed', ib.ID_Group):
            return {"Error": 403}
    elif not session.allowed('comments_allowed', ib.ID_Group):
        return {"Error": 403}

    try:
        new_comment = DB.Comment(ID_InfoBase=id_ib, ID_Account=session.account.ID_Account,
                                 Text=text, Attachments=attachment)

        DB.Ses.add(new_comment)
        DB.Ses.commit()

        notificationManager.send_notification_comment(ib, 'New answer in ' + ib.Title + ': ' + new_comment.Text)

        return {"Success": True}

    except Exception as e:
        print(e)
        DB.Ses.rollback()
        return {"Error": "DB error"}


@api.delete("/delete_comment")
def dgfdregergerged(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    comment = DB.Ses.query(DB.Comment).where(int(payload['id_comment']) == DB.Comment.ID_Comment).first()

    if not comment:
        return {"Error": 404}

    if not (session.allowed("moderate_comments", comment.infobase.ID_Group)
            or session.account.ID_Account == comment.ID_Account):
        return {"Error": 403}

    try:
        DB.Ses.delete(comment)
        DB.Ses.commit()

        return {"Success": True}

    except Exception as e:
        print(e)
        DB.Ses.rollback()
        return {"Error": "Not a success"}


@api.post("/rate")
def ppbghrc(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    if not session:
        return {"Error": "Go to 3 happy letters!"}

    rank = int(payload['Rank'])

    if rank not in range(1, 6):
        return {"Error": 412}

    try:
        rate = (DB.Ses.query(DB.Rank).where
                (DB.Rank.ID_Account == int(session.account.ID_Account) and
                 DB.Rank.ID_InfoBase == int(payload["ID_InfoBase"]))).first()

        if rate:
            DB.Ses.delete(rate)
            DB.Ses.commit()

        rate = DB.Rank(
            ID_InfoBase=payload['ID_InfoBase'],
            ID_Account=session.account.ID_Account,
            Value=rank
        )

        DB.Ses.add(rate)

        ib = DB.Ses.query(DB.InfoBase).where(int(payload['ID_InfoBase']) == DB.InfoBase.ID_InfoBase).first()

        sum = 0.0
        for i in ib.rates:
            sum += float(i.Value)

        ib.Rate = sum / float(len(ib.rates))

        DB.Ses.commit()

        return {"Success": True}

    except Exception as e:
        print(e)
        DB.Ses.rollback()
        return {"Error": "500"}

from fastapi import FastAPI, Body

import API.AuthSession as AuthSession
import DB

api = FastAPI()


@api.post('/get_comments')
def fef(payload: dict = Body(...)):
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
            "Text": comment.Text,
            "Rank": comment.Rank,
            "Attachments": comment.Attachments
        })

    return answer


@api.delete("/delete_comment")
def ded(payload: dict = Body(...)):
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
    except Exception as e:
        print(e)
        DB.Ses.rollback()

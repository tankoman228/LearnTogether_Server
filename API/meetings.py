from fastapi import FastAPI, Body

import DB

from API import AuthSession
from API.Notifications import notificationManager

app = FastAPI()


@app.post('/get_meetings')
def fef(payload: dict = Body(...)):
    if str(payload['session_token']) not in AuthSession.auth_sessions.keys():
        return {"Error": 'Unregistered'}

    group = int(payload['group'])
    search_str = payload['search_string']
    number = int(payload['number'])

    try:
        id_max = int(payload['id_max'])
    except:
        id_max = 99999999999

    db_session = DB.create_session()

    try:
        meetings = (db_session.query(DB.Meeting).join(DB.InfoBase).filter(
            DB.InfoBase.ID_Group == group, DB.InfoBase.ID_InfoBase <= id_max).
                    order_by(DB.Meeting.ID_Meeting.desc()).limit(number).all())

        result = []

        for meeting in meetings:

            if search_str in meeting.infobase.Title:
                result.append({
                    'ID_Meeting': meeting.ID_Meeting,
                    'ID_InfoBase': meeting.ID_InfoBase,
                    'Place': meeting.Place,
                    'Title': meeting.infobase.Title,
                    'Text': meeting.infobase.Text,
                    'WhenAdd': str(meeting.infobase.WhenAdd),
                    'Rate': meeting.infobase.Rate,
                    "CommentsFound": len(meeting.infobase.comments),
                    "PeopleJoined": len(meeting.responses),
                    "AuthorTitle": meeting.infobase.account.Title,
                    "StartsAt": str(meeting.Starts)
                })
                continue

            for tag in meeting.infobase.tags:
                if search_str in tag.tag.Text:
                    result.append({
                        'ID_Meeting': meeting.ID_Meeting,
                        'ID_InfoBase': meeting.ID_InfoBase,
                        'Place': meeting.Place,
                        'Title': meeting.infobase.Title,
                        'Text': meeting.infobase.Text,
                        'WhenAdd': str(meeting.infobase.WhenAdd),
                        'Rate': meeting.infobase.Rate,
                        "CommentsFound": len(meeting.infobase.comments),
                        "PeopleJoined": len(meeting.responses),
                        "AuthorTitle": meeting.infobase.account.Title,
                        "StartsAt": str(meeting.Starts)
                    })
                    break

        db_session.close()
        return {"Meetings": result}

    except Exception as e:
        db_session.rollback()
        db_session.close()
        print(e)
        return {"Error": str(e)}


@app.post('/get_meeting')
def fef(payload: dict = Body(...)):
    if str(payload['session_token']) not in AuthSession.auth_sessions.keys():
        return {"Error": 'Unregistered'}

    id_meeting = int(payload['id_object'])

    db_session = DB.create_session()

    try:
        meeting = db_session.query(DB.Meeting).filter(DB.Meeting.ID_Meeting == id_meeting).first()

        responses_list = []
        for response in meeting.responses:
            responses_list.append({
                'Account': response.account.Title,
                'Surety': response.Surety,
                'Start': response.Start,
                'End': response.End
            })

        db_session.close()
        return {"Results": responses_list}

    except Exception as e:
        db_session.rollback()
        db_session.close()
        print(e)
        return {"Error": "Error"}


@app.post('/join_meeting')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    if not session:
        return {"Error": "I'm a teapot"}

    id_meeting = int(payload['id_object'])

    db_session = DB.create_session()

    try:
        meeting = db_session.query(DB.Meeting).filter(DB.Meeting.ID_Meeting == id_meeting).first()

        if not meeting:
            return {"Error": "I'm not a teapot"}

        resp = db_session.query(DB.MeetingRespond).filter(
            (DB.MeetingRespond.ID_Meeting == id_meeting) &
            (DB.MeetingRespond.ID_Account == int(session.account.ID_Account)).first()
        )

        if resp:
            db_session.delete(resp)
            db_session.commit()

        respond = DB.MeetingRespond(
            ID_Account=session.account.ID_Account,
            ID_Meeting=id_meeting,
            Surety=float(payload['Surety']),
            Start=payload['starts'],
            End=payload['End']
        )
        db_session.add(respond)
        db_session.commit()
        db_session.close()

        return {"Success": True}

    except Exception as e:
        print('server error: ', e)
        db_session.rollback()
        db_session.close()
        return {"Error": "Error"}

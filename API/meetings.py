from fastapi import FastAPI, Body

import DB

from API import AuthSession

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

    meetings = (DB.Ses.query(DB.Meeting).join(DB.InfoBase).where(
        DB.InfoBase.ID_Group == group and DB.InfoBase.ID_InfoBase <= id_max).
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
                "StartsAt": meeting.infobase.account.Title
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
                    "StartsAt": meeting.infobase.account.Title
                })
                break

    return {"Meetings": result}


@app.post('/get_meeting')
def fef(payload: dict = Body(...)):
    if str(payload['session_token']) not in AuthSession.auth_sessions.keys():
        return {"Error": 'Unregistered'}

    id_meeting = int(payload['ID_Meeting'])

    meeting = DB.Ses.query(DB.Meeting).where(DB.Meeting.ID_Meeting == id_meeting).first()

    responses_list = []
    for response in meeting.responses:
        responses_list.append({
            'Account': response.account.Title,
            'Surety': response.Surety,
            'Start': response.Start,
            'End': response.End,
            'Reason': response.Reason
        })

    return {"Responds": responses_list}


@app.post('/join_meeting')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    if not session:
        return {"Error": "I'm a teapot"}

    id_meeting = int(payload['ID_Meeting'])
    meeting = DB.Ses.query(DB.Meeting).where(DB.Meeting.ID_Meeting == id_meeting).first()

    if not meeting:
        return {"Error": "I'm not a teapot"}

    try:

        respond = DB.MeetingRespond(
            ID_Account=session.account.ID_Account,
            ID_Meeting=id_meeting,
            Surety=float(payload['Surety']),
            Start=payload['Start'],
            End=payload['End'],
            Reason=payload['Reason']
        )
        DB.Ses.add(respond)
        DB.Ses.commit()

        return {"Success": "Result"}

    except Exception as e:

        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}

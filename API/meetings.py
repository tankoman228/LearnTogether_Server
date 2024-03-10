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
                "StartsAt": meeting.Starts
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
                    "StartsAt": meeting.Starts
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

        resp = DB.Ses.query(DB.MeetingRespond).filter(
            (DB.MeetingRespond.ID_Meeting == id_meeting) &
            (DB.MeetingRespond.ID_Account == int(session.account.ID_Account))).first()
        if resp:
            DB.Ses.delete(resp)
            DB.Ses.commit()

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


@app.post('/add_meeting')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    if not session:
        return {"Error": "I'm a teapot"}
    else:
        try:
            session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

            id_group = payload["id_group"]
            title = payload["title"]
            text = payload["text"]
            tags = payload["tags"].replace(' ', '').split(',')
            starts = payload["starts"]
            place = payload["place"]

            tags_id = []

            if not session.allowed("offer_publications", id_group):
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

            ib = DB.InfoBase(ID_Group=id_group, ID_Account=session.account.ID_Account, Title=title, Text=text, Type='m')
            DB.Ses.add(ib)
            DB.Ses.commit()

            for tid in tags_id:
                DB.Ses.add(DB.InfoTag(ID_Tag=tid, ID_InfoBase=ib.ID_InfoBase))
                DB.Ses.commit()

            DB.Ses.add(DB.Meeting(
                ID_InfoBase=ib.ID_InfoBase,
                Starts=starts,
                Place=place
            ))
            DB.Ses.commit()

            notificationManager.send_notifications(id_group, f'New meeting in {place} at {starts}')

            return {"Success": "Success!"}

        except Exception as e:

            print('server error: ', e)
            DB.Ses.rollback()
            return {"Error": "Error"}

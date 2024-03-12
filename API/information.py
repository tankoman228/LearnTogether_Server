from fastapi import FastAPI, Body

import DB
from API import AuthSession
from API.Notifications import notificationManager

app = FastAPI()


@app.post('/get_infos')
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

    infos = (DB.Ses.query(DB.Information).join(DB.InfoBase).where(
        DB.InfoBase.ID_Group == group and DB.InfoBase.ID_InfoBase <= id_max).
            order_by(DB.Information.ID_Information.desc()).limit(number).all())

    result = []

    for info in infos:

        if search_str in info.infobase.Title:
            result.append({
                'ID_Information': info.ID_Information,
                'ID_InfoBase': info.ID_InfoBase,
                'Type': info.Type,
                'Title': info.infobase.Title,
                'Text': info.infobase.Text,
                'WhenAdd': str(info.infobase.WhenAdd),
                'Rate': info.infobase.Rate,
                "CommentsFound": len(info.infobase.comments),
                "AuthorTitle": info.infobase.account.Title
            })
            continue

        for tag in info.infobase.tags:
            if search_str in tag.tag.Text:
                result.append({
                    'ID_Information': info.ID_Information,
                    'ID_InfoBase': info.ID_InfoBase,
                    'Type': info.Type,
                    'Title': info.infobase.Title,
                    'Text': info.infobase.Text,
                    'WhenAdd': str(info.infobase.WhenAdd),
                    'Rate': info.infobase.Rate,
                    "CommentsFound": len(info.infobase.comments),
                    "AuthorTitle": info.infobase.account.Title
                })
                break

    return {"Infos": result}


@app.post('/download')
def fef(payload: dict = Body(...)):

    if str(payload['session_token']) not in AuthSession.auth_sessions.keys():
        return {"Error": 'Unregistered'}

    return {
        "Contents":
        DB.Ses.query(DB.Information).where(int(payload['ID']) == DB.Information.ID_Information).first().Contents}


@app.post('/add_info')
def fef(payload: dict = Body(...)):

    try:
        session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

        id_group = payload["id_group"]
        title = payload["title"]
        text = payload["text"]
        tags = payload["tags"].replace(' ', '').split(',')
        contents = payload["contents"]
        type_ = str(payload["type"])[0]

        tags_id = []

        if not session.allowed("moderate_publications", id_group):
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

        ib = DB.InfoBase(ID_Group=id_group, ID_Account=session.account.ID_Account, Title=title, Text=text, Type='i')
        DB.Ses.add(ib)
        DB.Ses.commit()

        for tid in tags_id:
            DB.Ses.add(DB.InfoTag(ID_Tag=tid, ID_InfoBase=ib.ID_InfoBase))
            DB.Ses.commit()

        DB.Ses.add(DB.Information(
            ID_InfoBase=ib.ID_InfoBase,
            Contents=contents,
            Type=type_
        ))
        DB.Ses.commit()

        notificationManager.send_notifications(id_group, 'New material: ' + ib.Title)

        return {"Success": True}

    except Exception as e:

        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}

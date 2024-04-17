from fastapi import FastAPI, Body

import DB
from API import AuthSession
from API.Notifications import notificationManager

app = FastAPI()


@app.post('/get_infos')
def fef(payload: dict = Body(...)):
    db_session = DB.create_session()

    try:
        if str(payload['session_token']) not in AuthSession.auth_sessions.keys():
            db_session.close()
            return {"Error": 'Unregistered'}

        group = int(payload['group'])
        search_str = payload['search_string']
        number = int(payload['number'])

        try:
            id_max = int(payload['id_max'])
        except:
            id_max = 99999999999

        infos = (db_session.query(DB.Information).join(DB.InfoBase).filter(
            DB.InfoBase.ID_Group == group, DB.InfoBase.ID_InfoBase <= id_max).
                order_by(DB.Information.ID_Information.desc()).limit(number).all())

        result = []

        for info in infos:

            if search_str in info.infobase.Title:
                result.append({
                    'ID_Information': info.ID_Information,
                    'ID_InfoBase': info.ID_InfoBase,
                    'ID_Account': info.infobase.account.ID_Account,
                    'Type': info.Type,
                    'Title': info.infobase.Title,
                    'Text': info.infobase.Text,
                    'WhenAdd': str(info.infobase.WhenAdd),
                    'Rate': info.infobase.Rate,
                    "CommentsFound": len(info.infobase.comments),
                    "AuthorTitle": info.infobase.account.Title,
                    "Icon": info.infobase.account.Icon
                })
                continue

            for tag in info.infobase.tags:
                if search_str in tag.tag.Text:
                    result.append({
                        'ID_Information': info.ID_Information,
                        'ID_InfoBase': info.ID_InfoBase,
                        'ID_Account': info.infobase.account.ID_Account,
                        'Type': info.Type,
                        'Title': info.infobase.Title,
                        'Text': info.infobase.Text,
                        'WhenAdd': str(info.infobase.WhenAdd),
                        'Rate': info.infobase.Rate,
                        "CommentsFound": len(info.infobase.comments),
                        "AuthorTitle": info.infobase.account.Title,
                        "Icon": info.infobase.account.Icon
                    })
                    break

        db_session.close()
        return {"Infos": result}

    except Exception as e:
        db_session.rollback()
        db_session.close()
        print(e)
        return {"Error": "Error"}


@app.post('/download')
def fef(payload: dict = Body(...)):
    db_session = DB.create_session()

    try:
        if str(payload['session_token']) not in AuthSession.auth_sessions.keys():
            db_session.close()
            return {"Error": 'Unregistered'}

        info = db_session.query(DB.Information).filter(DB.Information.ID_Information == int(payload['id_object'])).first()

        db_session.close()
        return {"Contents": info.Contents}

    except Exception as e:
        db_session.close()
        print(e)
        return {"Error": "Error"}


@app.post('/add_info')
def fef(payload: dict = Body(...)):

    try:
        db_session = DB.create_session()

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
            db_tag = db_session.query(DB.Tag).where(str(tag) == DB.Tag.Text).first()
            if db_tag:
                tags_id.append(db_tag.ID_Tag)
            else:
                new_tag = DB.Tag(Text=tag)
                db_session.add(new_tag)
                db_session.commit()

                tags_id.append(new_tag.ID_Tag)

        ib = DB.InfoBase(ID_Group=id_group, ID_Account=session.account.ID_Account, Title=title, Text=text, Type='i')
        db_session.add(ib)
        db_session.commit()

        for tid in tags_id:
            db_session.add(DB.InfoTag(ID_Tag=tid, ID_InfoBase=ib.ID_InfoBase))
            db_session.commit()

        db_session.add(DB.Information(
            ID_InfoBase=ib.ID_InfoBase,
            Contents=contents,
            Type=type_
        ))
        db_session.commit()

        notificationManager.send_notifications(id_group, 'New material: ' + ib.Title)

        return {"Success": True}

    except Exception as e:
        print('server error: ', e)
        db_session.rollback()
        db_session.close()
        return {"Error": "Error"}
from fastapi import FastAPI, Body

import DB
import API.AuthSession as AuthSession
import API.Notifications.notificationManager as notify

app = FastAPI()


@app.post('/get_news')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    if not session:
        return {"Error": "Wenomechainsama"}

    group = int(payload['group'])
    search_str = str(payload['search_string'])
    number = int(payload['number'])

    is_moderator = session.allowed('moderate_publications', group)

    try:
        id_max = int(payload['id_max'])
    except:
        id_max = 99999999999

    news = (DB.Ses.query(DB.News).where(DB.InfoBase.ID_Group == group and DB.InfoBase.ID_InfoBase <= id_max and
                                        (DB.News.Moderated or is_moderator))
            .order_by(DB.News.ID_News.desc()).limit(number).all())

    tasks = (DB.Ses.query(DB.Task).where(DB.InfoBase.ID_Group == group and DB.InfoBase.ID_InfoBase <= id_max and
                                         (DB.Task.Moderated or is_moderator))
             .order_by(DB.Task.ID_Task.desc()).limit(number).all())

    votes = (DB.Ses.query(DB.Vote).where(DB.InfoBase.ID_Group == group and DB.InfoBase.ID_InfoBase <= id_max and
                                         (DB.Vote.Moderated or is_moderator))
             .order_by(DB.Vote.ID_Vote.desc()).limit(number).all())

    news_json = []
    tasks_json = []
    votes_json = []

    for i in news:

        if search_str in i.infobase.Title:
            news_json.append({
                'ID_News': i.ID_News,
                'ID_InfoBase': i.ID_InfoBase,
                'Title': i.infobase.Title,
                'Images': i.Images,
                'Moderated': i.Moderated,
                'Text': i.infobase.Text,
                'WhenAdd': str(i.infobase.WhenAdd),
                'Rate': i.infobase.Rate,
                "CommentsFound": len(i.infobase.comments),
                "AuthorTitle": i.infobase.account.Title
            })
            continue

        for tag in i.infobase.tags:
            if search_str in tag.tag.Text:
                news_json.append({
                    'ID_News': i.ID_News,
                    'ID_InfoBase': i.ID_InfoBase,
                    'Title': i.infobase.Title,
                    'Images': i.Images,
                    'Moderated': i.Moderated,
                    'Text': i.infobase.Text,
                    'WhenAdd': str(i.infobase.WhenAdd),
                    'Rate': i.infobase.Rate,
                    "CommentsFound": len(i.infobase.comments),
                    "AuthorTitle": i.infobase.account.Title
                })
                break

    for i in tasks:

        if search_str in i.infobase.Title:
            tasks_json.append({
                'ID_News': i.ID_News,
                'ID_InfoBase': i.ID_InfoBase,
                'Title': i.infobase.Title,
                'Deadline': i.Deadline,
                'Moderated': i.Moderated,
                'Text': i.infobase.Text,
                'WhenAdd': str(i.infobase.WhenAdd),
                'Rate': i.infobase.Rate,
                "CommentsFound": len(i.infobase.comments),
                "AuthorTitle": i.infobase.account.Title
            })
            continue

        for tag in i.infobase.tags:
            if search_str in tag.tag.Text:
                tasks_json.append({
                    'ID_News': i.ID_News,
                    'ID_InfoBase': i.ID_InfoBase,
                    'Title': i.infobase.Title,
                    'Deadline': i.Deadline,
                    'Moderated': i.Moderated,
                    'Text': i.infobase.Text,
                    'WhenAdd': str(i.infobase.WhenAdd),
                    'Rate': i.infobase.Rate,
                    "CommentsFound": len(i.infobase.comments),
                    "AuthorTitle": i.infobase.account.Title
                })
                break

    for i in votes:

        if search_str in i.infobase.Title:
            votes_json.append({
                'ID_News': i.ID_News,
                'ID_InfoBase': i.ID_InfoBase,
                'Title': i.infobase.Title,
                'Anonymous': i.Anonymous,
                'Chosen': len(i.items.vote_accounts),
                'Moderated': i.Moderated,
                'Text': i.infobase.Text,
                'WhenAdd': str(i.infobase.WhenAdd),
                'Rate': i.infobase.Rate,
                "CommentsFound": len(i.infobase.comments),
                "AuthorTitle": i.infobase.account.Title
            })
            continue

        for tag in i.infobase.tags:
            if search_str in tag.tag.Text:
                votes_json.append({
                    'ID_News': i.ID_News,
                    'ID_InfoBase': i.ID_InfoBase,
                    'Title': i.infobase.Title,
                    'Anonymous': i.Anonymous,
                    'Chosen': len(i.items.vote_accounts),
                    'Moderated': i.Moderated,
                    'Text': i.infobase.Text,
                    'WhenAdd': str(i.infobase.WhenAdd),
                    'Rate': i.infobase.Rate,
                    "CommentsFound": len(i.infobase.comments),
                    "AuthorTitle": i.infobase.account.Title
                })
                break

    #
    return {'news': news_json, 'tasks': tasks_json, 'votes': votes_json}


@app.post('/accept_news')
def fef(payload: dict = Body(...)):

    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    id_group = int(payload['group'])

    if not session or not session.allowed('moderate_publications', id_group):
        return {'Error': 'Not allowed'}

    try:
        type_ = str(payload['type'])
        id = int(payload['id'])
        #

        if type_ == 'n':

            news = DB.Ses.query(DB.News).where(DB.News.ID_News == id and DB.News.infobase.ID_Group == id_group).first()

            news.Moderated = True
            DB.Ses.commit()

            notify.send_notifications(id_group, f'News: {news.infobase.Title}')

        elif type_ == 't':

            task = DB.Ses.query(DB.Task).where(DB.Task.ID_Task == id and DB.Task.infobase.ID_Group == id_group).first()

            task.Moderated = True
            DB.Ses.commit()

            notify.send_notifications(id_group, f'New task: {task.infobase.Title}. Deadline is {str(task.Deadline)}')

        elif type_ == 'v':

            vote = DB.Ses.query(DB.Vote).where(DB.Vote.ID_Vote == id and DB.Vote.infobase.ID_Group == id_group).first()

            vote.Moderated = True
            DB.Ses.commit()

            notify.send_notifications(id_group, f'Vote: {vote.infobase.Title}')

        else:
            return {"Error": "Unknown type"}

    except Exception as e:
        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Server error"}


@app.post('/add_news')
def fef(payload: dict = Body(...)):

    try:
        session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

        id_group = payload["id_group"]
        title = payload["title"]
        text = payload["text"]
        tags = payload["tags"].replace(' ', '').split(',')
        images = payload["images"]
        is_moderator = session.allowed("moderate_publications", id_group)

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

        ib = DB.InfoBase(ID_Group=id_group, ID_Account=session.account.ID_Account, Title=title, Text=text, Type='n')
        DB.Ses.add(ib)
        DB.Ses.commit()

        for tid in tags_id:
            DB.Ses.add(DB.InfoTag(ID_Tag=tid, ID_InfoBase=ib.ID_InfoBase))
            DB.Ses.commit()

        DB.Ses.add(DB.News(
            ID_InfoBase=ib.ID_InfoBase,
            Images=images,
            Moderated=is_moderator
        ))
        DB.Ses.commit()

        if is_moderator:
            notify.send_notifications(id_group, f'News: {title}')
        else:
            notify.send_notifications_for_allowed(id_group, f'Need to review by moderator: {title}',
                                                  'moderate_publications')

        return {"Success": "Success!"}

    except Exception as e:

        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}


@app.post('/add_task')
def fef(payload: dict = Body(...)):

    try:
        session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

        id_group = payload["id_group"]
        title = payload["title"]
        text = payload["text"]
        tags = payload["tags"].replace(' ', '').split(',')
        deadline = payload["deadline"]
        is_moderator = session.allowed("moderate_publications", id_group)

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

        ib = DB.InfoBase(ID_Group=id_group, ID_Account=session.account.ID_Account, Title=title, Text=text, Type='n')
        DB.Ses.add(ib)
        DB.Ses.commit()

        for tid in tags_id:
            DB.Ses.add(DB.InfoTag(ID_Tag=tid, ID_InfoBase=ib.ID_InfoBase))
            DB.Ses.commit()

        DB.Ses.add(DB.Task(
            ID_InfoBase=ib.ID_InfoBase,
            Deadline=deadline,
            Moderated=is_moderator
        ))
        DB.Ses.commit()

        if is_moderator:
            notify.send_notifications(id_group, f'New task: {title}')
        else:
            notify.send_notifications_for_allowed(id_group, f'Need to review by moderator: {title}',
                                                  'moderate_publications')

        return {"Success": "Success!"}

    except Exception as e:

        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}


@app.post('/get_vote_info')
def fef(payload: dict = Body(...)):
    pass


@app.post('/add_vote')
def fef(payload: dict = Body(...)):
    pass


@app.post('/vote')
def fef(payload: dict = Body(...)):
    pass


@app.post('/update_task_status')
def wenomechainsama(payload: dict = Body(...)):
    pass

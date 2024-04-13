import os

from fastapi import FastAPI, Body
from sqlalchemy import and_

import DB
import API.AuthSession as AuthSession
import API.Notifications.notificationManager as notify

app = FastAPI()

from threading import Lock

# Создаем объект блокировки
session_lock = Lock()


@app.post('/get_news')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    try:
        DB.update_session()

        # ...
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

        news = (DB.Ses.query(DB.News).join(DB.InfoBase).join(DB.Account).filter(
            DB.InfoBase.ID_Group == group, DB.InfoBase.ID_InfoBase <= id_max,
            (DB.News.Moderated == True) | (is_moderator == True))
                .order_by(DB.News.ID_News.desc()).limit(number).all())

        tasks = (DB.Ses.query(DB.Task).join(DB.InfoBase).join(DB.Account).filter(
            DB.InfoBase.ID_Group == group, DB.InfoBase.ID_InfoBase <= id_max,
            (DB.Task.Moderated == True) | (is_moderator == True))
                 .order_by(DB.Task.ID_Task.desc()).limit(number).all())

        votes = (DB.Ses.query(DB.Vote).join(DB.InfoBase).join(DB.Account).filter(
            DB.InfoBase.ID_Group == group, DB.InfoBase.ID_InfoBase <= id_max,
            (DB.Vote.Moderated == True) | (is_moderator == True))
                 .order_by(DB.Vote.ID_Vote.desc()).limit(number).all())

        news_json = []
        tasks_json = []
        votes_json = []

        for i in news:
            if i is None:
                print('WTF error')
                continue

            if search_str in str(i.infobase.Title):

                try:
                    with open(i.Images, 'r') as file:
                        file_content = file.read()
                except:
                    print(i.Images, 'not found')
                    file_content = ''

                news_json.append({
                    'ID_News': i.ID_News,
                    'ID_InfoBase': i.ID_InfoBase,
                    'Title': i.infobase.Title,
                    'Images': file_content,
                    'Moderated': i.Moderated,
                    'Text': i.infobase.Text,
                    'WhenAdd': str(i.infobase.WhenAdd),
                    'Rate': i.infobase.Rate,
                    "CommentsFound": len(i.infobase.comments),
                    "AuthorTitle": i.infobase.account.Title,
                    "Avatar": i.infobase.account.Icon
                })
                continue

            for tag in i.infobase.tags:
                if search_str in tag.tag.Text:
                    try:
                        with open(i.Images, 'r') as file:
                            file_content = file.read()
                    except:
                        print(i.Images, 'not found')
                        file_content = ''

                    news_json.append({
                        'ID_News': i.ID_News,
                        'ID_InfoBase': i.ID_InfoBase,
                        'Title': i.infobase.Title,
                        'Images': file_content,
                        'Moderated': i.Moderated,
                        'Text': i.infobase.Text,
                        'WhenAdd': str(i.infobase.WhenAdd),
                        'Rate': i.infobase.Rate,
                        "CommentsFound": len(i.infobase.comments),
                        "AuthorTitle": i.infobase.account.Title,
                        "Avatar": i.infobase.account.Icon
                    })
                    break

        for i in tasks:

            if search_str in i.infobase.Title:
                tasks_json.append({
                    'ID_Task': i.ID_Task,
                    'ID_InfoBase': i.ID_InfoBase,
                    'Title': i.infobase.Title,
                    'Deadline': i.Deadline,
                    'Moderated': i.Moderated,
                    'Text': i.infobase.Text,
                    'WhenAdd': str(i.infobase.WhenAdd),
                    'Rate': i.infobase.Rate,
                    "CommentsFound": len(i.infobase.comments),
                    "AuthorTitle": i.infobase.account.Title,
                    "Avatar": i.infobase.account.Icon
                })
                continue

            for tag in i.infobase.tags:
                if search_str in tag.tag.Text:
                    tasks_json.append({
                        'ID_Task': i.ID_Task,
                        'ID_InfoBase': i.ID_InfoBase,
                        'Title': i.infobase.Title,
                        'Deadline': i.Deadline,
                        'Moderated': i.Moderated,
                        'Text': i.infobase.Text,
                        'WhenAdd': str(i.infobase.WhenAdd),
                        'Rate': i.infobase.Rate,
                        "CommentsFound": len(i.infobase.comments),
                        "AuthorTitle": i.infobase.account.Title,
                        "Avatar": i.infobase.account.Icon
                    })
                    break

        for i in votes:

            if search_str in i.infobase.Title:

                items = []
                for j in i.items:
                    items.append(str(j.Title))
                votes_json.append({
                    'ID_Vote': i.ID_Vote,
                    'ID_InfoBase': i.ID_InfoBase,
                    'Title': i.infobase.Title,
                    'Anonymous': i.Anonymous,
                    'Moderated': i.Moderated,
                    'Text': i.infobase.Text,
                    'WhenAdd': str(i.infobase.WhenAdd),
                    'Rate': i.infobase.Rate,
                    "CommentsFound": len(i.infobase.comments),
                    "AuthorTitle": i.infobase.account.Title,
                    "Items": items,
                    "Avatar": i.infobase.account.Icon
                })

                continue

            for tag in i.infobase.tags:
                if search_str in tag.tag.Text:
                    items = []
                    for j in i.items:
                        items.append(str(j.Title))
                    votes_json.append({
                        'ID_Vote': i.ID_Vote,
                        'ID_InfoBase': i.ID_InfoBase,
                        'Title': i.infobase.Title,
                        'Anonymous': i.Anonymous,
                        'Moderated': i.Moderated,
                        'Text': i.infobase.Text,
                        'WhenAdd': str(i.infobase.WhenAdd),
                        'Rate': i.infobase.Rate,
                        "CommentsFound": len(i.infobase.comments),
                        "AuthorTitle": i.infobase.account.Title,
                        "Items": items,
                        "Avatar": i.infobase.account.Icon
                    })
                    break

        #

        return {'news': news_json, 'tasks': tasks_json, 'votes': votes_json}

    except Exception as e:
        print(e)


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

        return {"Success": True}

    except Exception as e:
        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Server error"}


UPLOAD_FOLDER = 'uploads/'


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

        image_path = os.path.join('users_files', f'{ib.ID_InfoBase}' + '.txt')
        with open(image_path, 'w') as file:
            file.write(images)

        DB.Ses.add(DB.News(
            ID_InfoBase=ib.ID_InfoBase,
            Images=image_path,
            Moderated=is_moderator
        ))

        DB.Ses.commit()

        if is_moderator:
            notify.send_notifications(id_group, f'News: {title}')
        else:
            notify.send_notifications_for_allowed(id_group, f'Need to review by moderator: {title}',
                                                  'moderate_publications')

        return {"Success": True}

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

        ib = DB.InfoBase(ID_Group=id_group, ID_Account=session.account.ID_Account, Title=title, Text=text, Type='t')
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

        return {"Success": True}

    except Exception as e:

        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}


@app.post('/get_tasks_statuses')
def wenomechainsama(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    only_mine = payload['only_mine']

    if not session:
        return {"Error": "wenomechainsama!"}

    if only_mine:
        tasks = DB.Ses.query(DB.TaskAccount).where(DB.TaskAccount.ID_Account == int(session.account.ID_Account)).order_by(DB.TaskAccount.ID_Task.desc()).all()
    else:
        group = int(payload['id_group'])
        tasks = (DB.Ses.query(DB.TaskAccount).join(DB.Task).join(DB.InfoBase).
                 filter(DB.InfoBase.ID_Group == group).filter(DB.TaskAccount.ID_Task == int(payload['id_object'])).order_by(DB.TaskAccount.ID_Task.desc()).all())

    result = []

    for task in tasks:
        result.append({
            'ID_Task': task.ID_Task,
            'NeedHelp': task.NeedHelp,
            'Finished': task.Finished,
            'Priority': task.Priority,
            'AccountTitle': task.account.Title,
            'TaskTitle': task.task.infobase.Title,
            'Text': task.task.infobase.Text,
            'Deadline': str(task.task.Deadline)
        })

    print(result)
    return {'tasks': result}


@app.post('/update_task_status')
def wenomechainsama(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    todo = str(payload['todo'])

    if not session:
        return {"Error": "wenomechainsama!"}

    id_task = int(payload['ID_Task'])

    task = (DB.Ses.query(DB.TaskAccount).join(DB.Task).join(DB.InfoBase)
            .filter(DB.TaskAccount.ID_Account == int(session.account.ID_Account))
            .filter(DB.TaskAccount.ID_Task == id_task).first())

    try:
        if todo == 'delete':
            if not task:
                return {"Error": "Not exists"}
            else:
                DB.Ses.delete(task)
                DB.Ses.commit()
        elif todo == 'update_or_create':

            need_help = bool(payload['NeedHelp'])
            finished = bool(payload['Finished'])
            priority = int(payload['Priority'])

            if not task:
                task = DB.TaskAccount(
                    ID_Account=session.account.ID_Account,
                    ID_Task=id_task,
                    NeedHelp=need_help,
                    Finished=finished,
                    Priority=priority
                )
                DB.Ses.add(task)

                DB.Ses.commit()

            else:
                task.NeedHelp = need_help
                task.Finished = finished
                task.Priority = priority

                DB.Ses.commit()

            if need_help:
                notify.send_notifications(task.task.infobase.ID_Group,
                                          f'{session.account.Title} needs help to do {task.task.infobase.Title}!')

        return {"Success": True}

    except Exception as e:

        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}


@app.post('/get_vote_info')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    id_vote = int(payload['id_object'])

    vote = DB.Ses.query(DB.Vote).where(DB.Vote.ID_Vote == id_vote).first()
    result = []

    if not vote:
        return {"Error": "404"}

    if vote.Anonymous:
        for vote_item in vote.items:
            result.append({
                'Count': len(vote_item.vote_accounts),
                'Item': vote_item.Title
            })
    else:
        for vote_item in vote.items:
            for voteAccount in vote_item.vote_accounts:
                result.append({
                    'Name': voteAccount.account.Title,
                    'Item': vote_item.Title
                })

    return {'Results': result}


@app.post('/add_vote')
def fef(payload: dict = Body(...)):
    try:
        session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

        id_group = payload["id_group"]
        title = payload["title"]
        text = payload["text"]
        tags = payload["tags"].replace(' ', '').split(',')

        anon = payload['Anonymous']
        multianswer = payload['MultAnswer']
        items: [] = payload['items']

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

        vote = DB.Vote(
            ID_InfoBase=ib.ID_InfoBase,
            Moderated=is_moderator,
            Anonymous=anon,
            MultAnswer=multianswer
        )
        DB.Ses.add(vote)
        DB.Ses.commit()

        n = []
        for i in items:
            if i not in n:
                n.append(i)

        for item in n:
            DB.Ses.add(DB.VoteItem(ID_Vote=vote.ID_Vote, Title=item))
            DB.Ses.commit()

        if is_moderator:
            notify.send_notifications(id_group, f'New task: {title}')
        else:
            notify.send_notifications_for_allowed(id_group, f'New unchecked vote: {title}',
                                                  'moderate_publications')

        return {"Success": True}

    except Exception as e:

        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}


@app.post('/vote')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    vote_items = payload['items']
    id_vote = int(payload['id_object'])

    print(payload)

    vote = DB.Ses.query(DB.Vote).where(DB.Vote.ID_Vote == id_vote).first()
    if not vote:
        return {"Error": "404"}

    try:
        votes = DB.Ses.query(DB.VoteAccount).where(int(session.account.ID_Account) == DB.VoteAccount.ID_Account).all()

        for vote_ in votes:
            DB.Ses.delete(vote_)
            DB.Ses.commit()

        if len(vote_items) == 0:
            return {"Error": "No selected items!"}
        if not vote.MultAnswer and len(vote_items) > 1:
            return {"Error": "Too much selected items!"}

        for item in vote_items:
            id_item = DB.Ses.query(DB.VoteItem).filter(
                and_(DB.VoteItem.ID_Vote == id_vote, DB.VoteItem.Title == item)
            ).first().ID_VoteItem

            print(item, id_item)
            DB.Ses.add(DB.VoteAccount(
                ID_VoteItem=id_item,
                ID_Account=session.account.ID_Account
            ))
            DB.Ses.commit()

        return {"Success": True}

    except Exception as e:

        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}

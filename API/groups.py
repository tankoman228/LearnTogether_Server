from fastapi import FastAPI, Body

import DB
import API.AuthSession as AuthSession

api = FastAPI()


@api.post('/get_groups')
def sdc(payload: dict = Body(...)):
    db_session = DB.create_session()  # Создание сессии

    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    answer = {"Results": []}

    account_groups = db_session.query(DB.AccountGroup).filter(
        DB.AccountGroup.ID_Account == int(session.account.ID_Account)).all()
    for account_group in account_groups:
        answer["Results"].append(account_group.group)

    db_session.close()  # Закрытие сессии
    return answer


@api.post("/get_users")
def sdc(payload: dict = Body(...)):
    db_session = DB.create_session()  # Create a new session

    try:
        session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

        id_group = int(payload["group"])

        answer = {"users": []}

        account_groups = db_session.query(DB.AccountGroup).filter(DB.AccountGroup.ID_Group == id_group).all()
        for account_group in account_groups:
            account = db_session.query(DB.Account).filter(DB.Account.ID_Account == int(account_group.ID_Account)).first()
            answer["users"].append({

                'ID_Account': account.ID_Account,
                'Username': account.Username,
                'Title': account.Title,
                'Icon': account.Icon,
                'About': account.About,
                'Rating': account.Rating,
                'LastSeen': account.LastSeen,

                'Role': account_group.role.Name,
                'IsAdmin': account_group.role.IsAdmin
            })

        db_session.close()
        return answer

    except Exception as e:
        db_session.rollback()
        db_session.close()
        print(e)


@api.post("/join_group")
def join(payload: dict = Body(...)):
    db_session = DB.create_session()  # Create a new session

    try:
        session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
        token = db_session.query(DB.RegisterToken).filter(DB.RegisterToken.Text == str(payload['token'])).first()

        if token:

            if token.ID_Group in session.groups_id:
                return {"Error": "Already in group"}

            db_session.add(DB.AccountGroup(
                ID_Group=token.ID_Group,
                ID_Account=session.account.ID_Account,
                ID_Role=token.ID_Role
            ))
            db_session.delete(token)
            try:
                db_session.commit()
            except Exception as e:
                print(e)
                db_session.rollback()

            session.reload_groups_list()

            return {"Success!": True}

        return {"Error": "Invalid Token"}

    except Exception as e:
        db_session.rollback()
        db_session.close()
        print(e)


@api.post("/edit_group")
def join(payload: dict = Body(...)):
    db_session = DB.create_session()  # Create a new session

    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    id_group = int(payload['group'])

    if not session.allowed("edit_group", id_group):
        db_session.close()
        return {"Error": "Forbidden"}

    try:
        group = db_session.query(DB.Group).filter(DB.Group.ID_Group == id_group).first()

        if "NewName" in payload.keys():
            group.Name = payload["NewName"]
        if "NewIcon" in payload.keys():
            group.Icon = payload["NewIcon"]
        if "NewDescription" in payload.keys():
            group.Description = payload["NewDescription"]

        db_session.commit()

        return {"Success": True}

    except Exception as e:
        print('server error: ', e)
        db_session.rollback()
        db_session.close()
        return {"Error": "Error"}


@api.post("/edit_profile")
def ep(payload: dict = Body(...)):
    db_session = DB.create_session()
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    try:
        account = db_session.query(DB.Account).filter(DB.Account.ID_Account == int(session.account.ID_Account)).first()

        account.Title = payload["NewName"]
        account.Icon = payload["NewIcon"]
        account.About = payload["NewDescription"]

        db_session.commit()
        db_session.close()

        return {"Success": True}

    except Exception as e:
        print('server error: ', e)
        db_session.rollback()
        db_session.close()
        return {"Error": "Error"}


@api.post("/my_account_info")
def ep(payload: dict = Body(...)):
    try:
        session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
        id_group = int(payload["id_group"])

        return {
            "Username": session.account.Username,
            "Title": session.account.Title,
            "Icon": session.account.Icon,
            "Text": session.account.About,
            "Items": session.group_permissions_cache[id_group],
            "Success": True
        }

    except Exception as e:
        print('server error: ', e)
        return {"Error": "Error"}

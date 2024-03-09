from fastapi import FastAPI, Body

import DB
from API import AuthSession
from API.Notifications import notificationManager

app = FastAPI()


@app.post('/get_roles')
def fef(payload: dict = Body(...)):

    if str(payload['session_token']) not in AuthSession.auth_sessions.keys():
        return {"Error": 'Unregistered'}

    roles = DB.Ses.query(DB.Role).all()

    answer = []
    for role in roles:
        permissions_list = []
        for permission in role.permissions:
            permissions_list.append(str(permission.Name))

        answer.append({
            "ID_Role": role.ID_Role,
            "Name": role.Name,
            "IsAdmin": role.IsAdmin,
            "AdminLevel": role.AdminLevel,
            "Permissions": permissions_list
        })


@app.post('/create_token')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    id_group = int(payload["ID_Group"])
    id_role = int(payload["ID_Role"])
    text = str(payload["Text"])

    sender_role = session.group_roles_cache[id_group]

    if not session.allowed("create_tokens", id_group) or not sender_role.IsAdmin:
        return {"Error": "Forbidden"}

    try:
        required_role = DB.Ses.query(DB.Role).where(DB.Role.ID_Role == id_role).first()

        for permission in required_role.permissions:
            if permission not in sender_role.permissions:
                return {"Error": "New user can't have permissions that you don't have now"}

        if required_role.IsAdmin and not sender_role.IsAdmin:
            return {"Error": "New user can't be admin because you are not"}

        if required_role.IsAdmin and required_role.AdminLevel > sender_role.AdminLevel:
            return {"Error": "New user can't be admin higher in hierarchy than you"}

        token = DB.RegisterToken(
            ID_Group=id_group,
            Text=text,
            ID_Role=id_role
        )

        DB.Ses.add(token)
        DB.Ses.commit()

        return {"Success": True}

    except Exception as e:

        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}


@app.post('/delete_ib')
def fef(payload: dict = Body(...)):

    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    id_ib = int(payload["ID_InfoBase"])
    info_base = DB.Ses.query(DB.InfoBase).where(DB.InfoBase.ID_InfoBase == id_ib).first()

    if (not session.allowed("moderate_publications", info_base.ID_Group) or
            not info_base.ID_account == session.account.ID_Account):
        return {"Error": "Forbidden"}

    try:
        DB.Ses.delete(info_base)
        DB.Ses.commit()
    except Exception as e:

        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}


@app.post('/change_user_role')
def fef(payload: dict = Body(...)):
    pass


@app.post('/new_role')
def fef(payload: dict = Body(...)):
    pass


@app.post('/edit_role')
def fef(payload: dict = Body(...)):
    pass


@app.post('/delete_role')
def fef(payload: dict = Body(...)):
    pass


@app.post('/block_account')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    id_account = int(payload["ID_Account"])
    id_group = int(payload["ID_Group"])

    ag = (DB.Ses.query(DB.AccountGroup).where
          (DB.AccountGroup.ID_Account == id_account and DB.AccountGroup.ID_Group == id_group)).first()

    if not session.allowed("ban_accounts", id_group):
        return {"Error": "Forbidden"}

    if ag.role.IsAdmin and ag.role.AdminLevel > session.group_roles_cache[id_group].AdminLevel:
        return {"Error": "You are lower in hierarchy than this user"}

    try:
        DB.Ses.delete(ag)
        DB.Ses.commit()

        for session_ in AuthSession.auth_sessions:
            if session_.account.ID_Account == id_account:
                session_.reload_groups_list()

    except Exception as e:

        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}


@app.post('/complaint')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    id_group = int(payload["ID_Group"])
    id_account = int(payload["ID_Account"])

    try:

        complaint = DB.Complaint(
            ID_Group=id_group,
            Sender=session.account.ID_Account,
            Suspected=id_account,
            Reason=payload['Reason'],
        )

        DB.Ses.add(complaint)
        DB.Ses.commit()

        notificationManager.send_notifications_for_admins(id_group, f'Complaint: {payload["Reason"]}')
        return {"Success": True}

    except Exception as e:

        print('server error: ', e)
        DB.Ses.rollback()
        return {"Error": "Error"}


@app.post('/get_complaints')
def fef(payload: dict = Body(...)):

    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    id_group = int(payload["ID_Group"])

    if not session.allowed("ban_accounts", id_group) or session.group_roles_cache[id_group].IsAdmin:
        return {"Error": "Forbidden"}

    complaints = DB.Ses.query(DB.Complaint).where(DB.Complaint.ID_Group == id_group).all()

    answer = []
    for complaint in complaints:
        answer.append({
            'ID_Complaint': complaint.ID_Complaint,
            'SenderID': complaint.sender.ID_Account,
            'SuspectedID': complaint.suspected.ID_Account,
            'Sender': complaint.sender.Title,
            'Suspected': complaint.suspected.Title,
            'Reason': complaint.Reason,
            'DateTime': str(complaint.DateTime)
        })

    return {"Complaints": answer}

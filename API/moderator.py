from fastapi import FastAPI, Body

import DB
from API import AuthSession
from API.Notifications import notificationManager

app = FastAPI()


@app.post('/get_roles')
def fef(payload: dict = Body(...)):
    if str(payload['session_token']) not in AuthSession.auth_sessions.keys():
        return {"Error": 'Unregistered'}

    db_session = DB.create_session()
    roles = db_session.query(DB.Role).all()

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

    db_session.close()
    return {"Roles": answer}


@app.post('/create_token')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    id_group = int(payload["ID_Group"])
    id_role = int(payload["ID_Role"])
    text = str(payload["text"])

    sender_role = session.group_roles_cache[id_group]

    if not session.allowed("create_tokens", id_group) or not sender_role.IsAdmin:
        return {"Error": "Forbidden"}

    db_session = DB.create_session()
    try:
        required_role = db_session.query(DB.Role).where(DB.Role.ID_Role == id_role).first()
        sender_role_permissions = []
        for p in sender_role.permissions:
            sender_role_permissions.append(p.Name)

        for permission in required_role.permissions:
            if permission.Name not in sender_role_permissions:
                return {"Error": "New user can't have permissions that you don't have now"}

        if required_role.IsAdmin and not sender_role.IsAdmin:
            return {"Error": "New user can't be admin because you are not"}

        if required_role.IsAdmin and (required_role.AdminLevel > sender_role.AdminLevel):
            return {"Error": "New user can't be admin higher in hierarchy than you"}

        token = DB.RegisterToken(
            ID_Group=id_group,
            Text=text,
            ID_Role=id_role
        )

        db_session.add(token)
        db_session.commit()

        db_session.close()
        return {"Success": True}

    except Exception as e:

        print('server error: ', e)
        db_session.rollback()
        db_session.close()
        return {"Error": "Error"}


@app.post('/get_tokens')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    id_group = int(payload["ID_Group"])
    sender_role = session.group_roles_cache[id_group]

    if not session.allowed("create_tokens", id_group) or not sender_role.IsAdmin:
        return {"Error": "Forbidden"}

    results = []

    db_session = DB.create_session()
    try:
        for token in db_session.query(DB.RegisterToken).where(DB.RegisterToken.ID_Group == id_group).all():

            flag_not_allowed = False

            required_role = token.role
            sender_role_permissions = []

            for p in sender_role.permissions:
                sender_role_permissions.append(p.Name)

            for permission in required_role.permissions:
                if permission.Name not in sender_role_permissions:
                    flag_not_allowed = True
                    break
            if flag_not_allowed:
                continue

            if required_role.IsAdmin and not sender_role.IsAdmin:
                continue

            if required_role.IsAdmin and (required_role.AdminLevel > sender_role.AdminLevel):
                continue

            t = token
            results.append(f'ID: {t.ID_RegisterToken} \t| Group[{t.group.ID_Group}]: {t.group.Name} '
                           f'\t| Role[{t.role.ID_Role}]: {t.role.Name} \t |  {t.Text}  |')

        db_session.close()
        return {"List": results}

    except Exception as e:

        print('server error: ', e)
        db_session.close()
        return {"Error": "Error"}


@app.post('/delete_ib')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    db_session = DB.create_session()

    id_ib = int(payload["ID_InfoBase"])
    info_base = db_session.query(DB.InfoBase).where(DB.InfoBase.ID_InfoBase == id_ib).first()

    if (not session.allowed("moderate_publications", info_base.ID_Group) and
            not info_base.ID_Account == session.account.ID_Account):
        return {"Error": "Forbidden"}

    try:
        db_session.delete(info_base)
        db_session.commit()

        db_session.close()
        return {"Success": True}

    except Exception as e:

        print('server error: ', e)
        db_session.rollback()
        db_session.close()
        return {"Error": "Error"}


@app.post('/change_user_role')
def change_user_role(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    id_group = int(payload["ID_Group"])
    id_role = int(payload["ID_Role"])
    id_account = int(payload["ID_Account"])

    db_session = DB.create_session()
    sender_role = session.group_roles_cache[id_group]
    target_role = db_session.query(DB.Role).where(DB.Role.ID_Role == id_role).first()
    current_role = db_session.query(DB.AccountGroup).filter(DB.AccountGroup.ID_Account == id_account and
                                                        DB.AccountGroup.ID_Group == id_group).first().role

    if current_role.AdminLevel > sender_role.AdminLevel:
        return {"Error": "Can't change users higher than you"}

    if int(session.account.ID_Account) == id_account:
        return {"Error": "Can't change yourself"}

    if not session.allowed('edit_roles', id_group):
        return {"Error": "Forbidden"}

    try:

        if not sender_role.IsAdmin and target_role.IsAdmin:
            return {"Error": "User can't be admin because you are not"}

        if sender_role.IsAdmin and target_role.IsAdmin and target_role.AdminLevel > sender_role.AdminLevel:
            return {"Error": "User can't be made higher than you"}

        sender_role_permissions = []
        for permission in sender_role.permissions:
            sender_role_permissions.append(permission.Name)

        for permission in target_role.permissions:
            if permission.Name not in sender_role_permissions:
                return {"Error": "User can't have permissions that you don't have now"}

        ag = (db_session.query(DB.AccountGroup).where
              (DB.AccountGroup.ID_Account == id_account and DB.AccountGroup.ID_Group == id_group).first())

        ag.ID_Role = target_role.ID_Role
        db_session.commit()

        db_session.close()
        return {"Success": True}

    except Exception as e:
        print('server error: ', e)
        db_session.rollback()
        db_session.close()
        return {"Error": "Error"}


@app.post('/new_role')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    id_group = int(payload["ID_Group"])
    permissions: [] = payload['Items']

    for permission in permissions:
        if permission not in ['moderate_publications', 'offer_publications', 'edit_roles', 'edit_group',
                              'forum_allowed', 'comments_allowed', 'moderate_comments',
                              'create_tokens', 'ban_accounts']:
            return {"Error": "Unknown permission"}

    if not session.allowed('edit_roles', id_group):
        return {"Error": "Forbidden"}

    name = payload["Name"]
    is_admin = bool(payload["IsAdmin"])
    admin_level = int(payload["AdminLevel"])
    sender_role = session.group_roles_cache[id_group]

    if is_admin and not sender_role.IsAdmin:
        return {"Error": "User can't be admin because you are not"}

    if sender_role.IsAdmin and is_admin and admin_level > sender_role.AdminLevel:
        return {"Error": "User can't be made higher than you in hierarchy"}

    for permission in permissions:
        if not session.allowed(permission, id_group):
            return {"Error": "Can't make role with permissions you don't have"}

    db_session = DB.create_session()

    if db_session.query(DB.Role).where(DB.Role.Name == name).first():
        return {"Error": "Role with this name already exists"}

    try:

        role = DB.Role(
            Name=name,
            IsAdmin=is_admin,
            AdminLevel=admin_level
        )
        db_session.add(role)
        db_session.commit()

        for permission in permissions:
            db_session.add(DB.Permission(
                ID_Role=role.ID_Role,
                Name=permission
            ))
            db_session.commit()

        return {"Success": True}

    except Exception as e:

        print('server error: ', e)
        db_session.rollback()
        db_session.close()
        return {"Error": "Error 500"}


@app.post('/delete_role')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    id_role = int(payload["ID_Role"])
    id_group = int(payload["ID_Group"])

    if id_role in range(1, 3):
        return {"Error": "Can't delete system role"}

    db_session = DB.create_session()
    role = db_session.query(DB.Role).where(DB.Role.ID_Role == id_role).first()

    if not session.allowed('edit_roles', id_group):
        return {"Error": "Forbidden"}

    if db_session.query(DB.AccountGroup).where(
            DB.AccountGroup.ID_Role == id_role).first():
        return {"Error": "Can't delete role that is being used"}

    if role.IsAdmin and not session.group_roles_cache[id_group].IsAdmin:
        return {"Error": "Forbidden in this case"}

    if role.AdminLevel > session.group_roles_cache[id_group].AdminLevel:
        return {"Error": "Forbidden in this case :("}

    try:
        for p in role.permissions:
            db_session.delete(p)

        db_session.delete(role)
        db_session.commit()

        return {"Success": True}
    except Exception as e:

        print('server error: ', e)
        db_session.rollback()
        return {"Error": "Error"}


@app.post('/block_account')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    id_account = int(payload["ID_Account"])
    id_group = int(payload["ID_Group"])

    db_session = DB.create_session()
    ag = (db_session.query(DB.AccountGroup).join(DB.Role).filter
          (DB.AccountGroup.ID_Account == id_account).filter(DB.AccountGroup.ID_Group == id_group)).first()

    if not session.allowed("ban_accounts", id_group):
        return {"Error": "Forbidden"}

    if ag.role.AdminLevel > session.group_roles_cache[id_group].AdminLevel:
        return {"Error": "You are lower in hierarchy than this user"}

    if id_account == int(session.account.ID_Account):
        return {"Error": "Can't ban yourself"}

    try:
        db_session.delete(ag)
        db_session.commit()

        return {"Result": True}

    except Exception as e:

        print('server error: ', e)
        db_session.rollback()
        db_session.close()
        return {"Error": "Error"}


@app.post('/ban_account')
def fef(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    id_account = int(payload["ID_Account"])
    id_group = int(payload["ID_Group"])

    db_session = DB.create_session()
    ag = (db_session.query(DB.AccountGroup).join(DB.Role).filter
          (DB.AccountGroup.ID_Account == id_account).filter(DB.AccountGroup.ID_Group == id_group)).first()

    if not session.allowed("ban_accounts", id_group):
        return {"Error": "Forbidden"}

    if ag.role.AdminLevel > session.group_roles_cache[id_group].AdminLevel:
        return {"Error": "You are lower in hierarchy than this user"}

    if id_account == int(session.account.ID_Account):
        return {"Error": "Can't ban yourself"}

    try:
        ag.account.Password = 'BANNED'
        db_session.delete(ag)
        db_session.commit()

        return {"Result": True}

    except Exception as e:

        print('server error: ', e)
        db_session.rollback()
        db_session.close()
        return {"Error": "Error"}


@app.post('/complaint')
def fef(payload: dict = Body(...)):
    db_session = DB.create_session()
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    id_group = int(payload["ID_Group"])
    id_account = int(payload["ID_Account"])
    reason = str(payload['Reason']).replace('\n', ' ')

    try:

        complaint = DB.Complaint(
            ID_Group=id_group,
            Sender=session.account.ID_Account,
            Suspected=id_account,
            Reason=reason,
        )

        db_session.add(complaint)
        db_session.commit()

        notificationManager.send_notifications_for_admins(id_group, f'Complaint: {payload["Reason"]}')
        db_session.close()
        return {"Success": True}

    except Exception as e:

        print('server error: ', e)
        db_session.rollback()
        db_session.close()
        return {"Error": "Error"}


@app.post('/get_complaints')
def fef(payload: dict = Body(...)):
    db_session = DB.create_session()
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    id_group = int(payload["ID_Group"])

    complaints = db_session.query(DB.Complaint).filter(DB.Complaint.ID_Group == id_group).all()

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

    db_session.close()
    return {"Complaints": answer}

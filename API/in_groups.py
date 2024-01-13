from fastapi import FastAPI, Body

import DB
import API.AuthSession as AuthSession

api = FastAPI()


@api.post('/get_groups')
def sdc(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    answer = {"groups": []}

    account_groups = DB.Ses.query(DB.AccountGroup).where(DB.AccountGroup.ID_Account == int(session.account.ID_Account)).all()
    for account_group in account_groups:
        answer["groups"].append(account_group.group)

    return answer


@api.post("/get_users")
def sdc(payload: dict = Body(...)):
    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]

    id_group = int(payload["group"])
    search = str(payload["search"])

    answer = {"users": []}

    account_groups = DB.Ses.query(DB.AccountGroup).where(DB.AccountGroup.ID_Group == id_group).all()
    for account_group in account_groups:
        account = DB.Ses.query(DB.Account).where(int(DB.Account.ID_Account) == account_group.ID_Account).first()
        answer["users"].append({

            'ID_Account': account.ID_Account,
            'Username': account.Username,
            'Password': account.Password,
            'RecoveryContact': account.RecoveryContact,
            'Title': account.Title,
            'Icon': account.Icon,
            'About': account.About,
            'Rating': account.Rating,
            'LastSeen': account.LastSeen,

            'Role': account_group.role.Name,
            'IsAdmin': account_group.role.IsAdmin
        })

    return answer

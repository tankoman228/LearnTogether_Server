import random
import string

from fastapi import FastAPI, Body

import DB
import password_hash
from API.AuthSession import *

api = FastAPI()


def generate_random_string(length=128):
    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


@api.post('/auth')
def svc(payload: dict = Body(...)):

    account = DB.Ses.query(DB.Account).where(DB.Account.Username == str(payload['username'])).first()

    if account and password_hash.check_password(account.Password, payload['password']):

        token = generate_random_string()
        auth_sessions[token] = AuthSession(account)

        print("auth: ", token)
        return {"Result": "Success", "Token": token}

    return {"Result": "Declined"}


@api.post('/register')
def ghx(payload: dict = Body(...)):

    token = DB.Ses.query(DB.RegisterToken).where(DB.RegisterToken.Text == str(payload['token'])).first()

    if token:

        if DB.Ses.query(DB.Account).where(DB.Account.Username == str(payload['username'])).first():
            return {"Error": "This username is taken, Choose another one"}

        try:

            if (len(payload['username']) <= 1 or len(payload['password']) <= 1
                    or len(payload['contact']) <= 1 or len(payload['title']) <= 1):
                return {"Error": "Empty field(s)"}

            new_acc = DB.Account(Username=payload['username'],
                                 Password=password_hash.hash_password(payload['password']),
                                 RecoveryContact=payload['contact'],
                                 Title=payload['title'])

            DB.Ses.add(new_acc)

            DB.Ses.commit()

            ag = DB.AccountGroup(ID_Group=token.ID_Group, ID_Role=token.ID_Role, ID_Account=new_acc.ID_Account)
            DB.Ses.add(ag)

            DB.Ses.delete(token)
            DB.Ses.commit()

            token = generate_random_string()
            auth_sessions[token] = AuthSession(new_acc)

            return {"Result": "Success", "Token": token}

        except Exception as e:
            print(e)
            DB.Ses.rollback()
            return {"Error": "Unknown error"}

    return {"Error": "No token found"}

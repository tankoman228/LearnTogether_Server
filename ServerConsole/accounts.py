import DB
import password_hash


def recover(args):
    if len(args) != 2:
        print('Wrong args! Right args are: recover <ID_Account|RecoveryContact> <New password>')
    else:
        session = DB.create_session()

        accounts = session.query(DB.Account).all()
        for account in accounts:
            try:
                if account.ID_Account == int(args[0]) or str(account.RecoveryContact).replace(" ", "") == str(args[0]):
                    account.Password = password_hash.hash_password(args[1])
                    session.commit()
                    session.close()
                    print("Success!")
                    return
            except:
                pass

        print("User not found")

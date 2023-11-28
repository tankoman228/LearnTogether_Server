from API.Session import Session


def debug_message(session: Session, text):
    print("debug message: ", text)
    if session.account is None:
        print('no_account')

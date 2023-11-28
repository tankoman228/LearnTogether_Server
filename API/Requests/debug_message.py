def debug_message(session, text):
    print("debug message: ", text[0])
    if session.account is None:
        print('no_account')
    session.send_data_to_user("debug: " + text[0])

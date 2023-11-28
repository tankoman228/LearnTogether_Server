def debug_message(session, args):
    print("debug message: ", args[0])
    if session.account is None:
        print('no_account')
    session.send_data_to_user("debug: " + args[0])

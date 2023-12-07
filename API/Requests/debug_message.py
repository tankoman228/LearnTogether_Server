def debug_message(session, args):
    print("debug message: ", args[0])
    if not session.account:
        session.send_data_to_user('no_account')
    session.send_data_to_user("debug: " + args[0])

    for s in session.other_sessions:
        if s != session:
            s.send_data_to_user("debug: " + args[0])

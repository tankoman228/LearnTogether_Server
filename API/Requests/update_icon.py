def update_icon(session, args):

    session.account.icon = args[0]
    #print(args)

    session.carma -= 100

    session.account.upd_profile()

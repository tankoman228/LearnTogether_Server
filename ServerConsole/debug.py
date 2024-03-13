import API.AuthSession as AuthSession
import API.Notifications.notificationManager
import DB


def create_session_token(args):

    if len(args) != 2:
        print('Wrong args number. You need to write: debug_token <token> <id_account>')
        return

    token = args[0]
    account = DB.Ses.query(DB.Account).where(DB.Account.ID_Account == int(args[1])).first()

    if not account:
        print("No account with such ID")
        return

    session = AuthSession.AuthSession(account)
    AuthSession.auth_sessions[token] = session
    AuthSession.notification_keys[token[0:15]] = session
    session.reload_groups_list()

    print(f'Success! Created token for account {account.Username} with {token}')


def send_debug_notification(args):

    if len(args) != 2:
        print('Wrong args number. You need to write: send_debug_notification <id_group> <text>')
        return

    API.Notifications.notificationManager.send_notifications(int(args[0]), args[1])
    print('Success')

import API.Notifications.NotificationChannels as nt
import DB

users_ids_notification_lists = {}


def send_notifications(id_group: int, notification: str):
    for user in DB.Ses.query(DB.AccountGroup).where(DB.AccountGroup.ID_Group == id_group).all():
        if user.ID_Account in users_ids_notification_lists.keys():
            users_ids_notification_lists[user.ID_Account].append(notification)
        else:
            users_ids_notification_lists[user.ID_Account] = [notification]


def send_notifications_for_allowed(id_group: int, notification: str, permission: str):
    for user in DB.Ses.query(DB.AccountGroup).where(DB.AccountGroup.ID_Group == id_group).all():

        allowed = False
        for p in user.role.permissions:
            if p.Name == permission:
                allowed = True
                break

        if not allowed:
            continue

        if user.ID_Account in users_ids_notification_lists.keys():
            users_ids_notification_lists[user.ID_Account].append(notification)
        else:
            users_ids_notification_lists[user.ID_Account] = [notification]


def send_notifications_for_admins(id_group: int, notification: str):
    for user in DB.Ses.query(DB.AccountGroup).where(DB.AccountGroup.ID_Group == id_group).all():

        if not user.role.IsAdmin:
            continue

        if user.ID_Account in users_ids_notification_lists.keys():
            users_ids_notification_lists[user.ID_Account].append(notification)
        else:
            users_ids_notification_lists[user.ID_Account] = [notification]


def send_notification_comment(ib: DB.InfoBase, notification: str):
    target_accounts = []
    comments = DB.Ses.query(DB.Comment).where(DB.Comment.ID_InfoBase == int(ib.ID_InfoBase))

    for comment in comments:
        if comment.ID_Account not in target_accounts:
            target_accounts.append(comment.ID_Account)

    for account in target_accounts:
        if account.ID_Account in users_ids_notification_lists.keys():
            users_ids_notification_lists[account.ID_Account].append(notification)
        else:
            users_ids_notification_lists[account.ID_Account] = [notification]
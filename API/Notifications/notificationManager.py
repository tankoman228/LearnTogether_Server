import API.Notifications.NotificationChannels as nt
import DB


def send_notifications(id_group: int, notification: str):

    for channel in nt.notification_tokens_channels.values():
        if id_group in channel.session.groups_id:
            channel.send_message(notification)


def send_notifications_for_allowed(id_group: int, notification: str, permission: str):

    for channel in nt.notification_tokens_channels.values():
        if id_group in channel.session.groups_id and channel.session.allowed(permission, id_group):
            channel.send_message(notification)


def send_notifications_for_admins(id_group: int, notification: str):

    for channel in nt.notification_tokens_channels.values():
        if id_group in channel.session.groups_id and channel.session.group_roles_cache[id_group].IsAdmin:
            channel.send_message(notification)


def send_notification_comment(ib: DB.InfoBase, notification: str):

    target_accounts = [int(ib.ID_Account)]
    comments = DB.Ses.query(DB.Comment).where(DB.Comment.ID_InfoBase == int(ib.ID_InfoBase))

    for comment in comments:
        if comment.ID_Account not in target_accounts:
            target_accounts.append(comment.ID_Account)

    for channel in nt.notification_tokens_channels.values():
        if ib.ID_Group in channel.session.account.groups_id:
            if channel.session.account.ID_Account in target_accounts:
                channel.send_message(notification)

import DB


class AuthSession:

    def __init__(self, account: DB.Account):

        self.account = account
        self.groups_id = []
        self.group_permissions_cache = {}
        self.reload_groups_list()

    def reload_groups_list(self):

        self.groups_id = []
        self.group_permissions_cache = {}

        ags = DB.Ses.query(DB.AccountGroup).where(DB.AccountGroup.ID_Account == int(self.account.ID_Account)).all()

        for ag in ags:
            self.groups_id.append(ag.ID_Group)
            self.group_permissions_cache[ag.ID_Group] = [str(permission.Name) for permission in ag.role.permissions]

    def allowed(self, permission_string: str, id_group: int):
        return permission_string in self.group_permissions_cache[id_group]


auth_sessions = {}
notification_keys = {}

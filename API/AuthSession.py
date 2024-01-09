import DB


class AuthSession:

    def __init__(self, account: DB.Account, group: DB.Group = None):
        self.account = account
        self.group = group
        self.role: DB.Role = None

        self.permissions = []
        self.recheck_permissions()

    def recheck_permissions(self):

        self.permissions = []

        if not self.group:
            ags = DB.Ses.query(DB.AccountGroup).where(DB.AccountGroup.ID_Account == int(self.account.ID_Account)).all()
            if len(ags) == 1:
                self.group = ags[0].group
            else:
                return

        self.role = DB.Ses.query(DB.AccountGroup).where(
            DB.AccountGroup.ID_Account == int(self.account.ID_Account) and
            DB.AccountGroup.ID_Group == int(self.group.ID_Group)
        ).first().role

        permissions = self.role.permissions
        for permission in permissions:
            self.permissions.append(permission.Name)

    def allowed(self, permission_string):
        return permission_string in self.permissions


auth_sessions = {}

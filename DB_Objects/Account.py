class Account:

    def __init__(self, username, password, recovery_contact,
                 title, icon, about, is_admin, admin_level,
                 rating, last_seen, id_user=-1):
        self.username = username
        self.password = password
        self.recovery_contact = recovery_contact
        self.title = title
        self.icon = icon
        self.about = about
        self.is_admin = is_admin
        self.admin_level = admin_level
        self.rating = rating
        self.last_seen = last_seen
        self.id = id_user

    def save_in_db(self):
        pass

    def delete_from_db(self):
        pass

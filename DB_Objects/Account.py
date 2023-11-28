import db_connection
import datetime

class Account:

    def __init__(self, username, password_hash, recovery_contact,
                 title, icon, about, is_admin, admin_level,
                 rating, last_seen, id_user=-1):
        self.username = username
        self.password_hash = password_hash
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
        try:
            with db_connection.connection.cursor() as cursor:

                if self.id == -1:
                    cursor.execute(
                        "INSERT INTO `Account` "
                        "(`Username`,`Password`,`RecoveryContact`,`Title`,`IsAdmin`,`AdminLevel`) "
                        "VALUES (%s,%s,%s,%s,%s,%s)",
                        (self.username,
                        self.password_hash,
                        self.recovery_contact,
                        self.title,
                        self.is_admin,
                        self.admin_level)
                        )
                    cursor.execute("SELECT MAX(`ID_Account`) FROM `Account`")
                    self.id = cursor.fetchone()[0]
                    self.last_seen = datetime.datetime.now()
                    db_connection.connection.commit()
                else:
                    print("to UPDATE `Account` use special methods, no save in DB")
                    return False
            return True
        except Exception as e:
            print(e)
            return False

    def upd_profile(self):
        with db_connection.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE `Account` SET `Title` = %s, `Icon` = %s, `About` = %s WHERE `ID_Account` = %s",
                (self.title, self.icon, self.about, self.id)
            )
            db_connection.connection.commit()

    def upd_rights(self):
        with db_connection.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE `Account` SET `IsAdmin` = %s, `AdminLevel` = %s WHERE `ID_Account` = %s",
                (self.is_admin, self.admin_level, self.id)
            )
            db_connection.connection.commit()

    def upd_status(self):
        with db_connection.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE `Account` SET `Rating` = %s, `LastSeen` = %s WHERE `ID_Account` = %s",
                (self.rating, self.last_seen, self.id)
            )
            db_connection.connection.commit()

    def delete_from_db(self):
        print("You can't delete accounts")

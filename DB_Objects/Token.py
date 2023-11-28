import hashlib
import password_hash
import db_connection
import DB_Queries.QueryStrings as q


class Token:

    #select from
    def __init__(self, id_group, text, is_admin, admin_level, id_token =-1):
        self.text = str(text)
        self.is_admin = bool(is_admin)
        self.admin_level = admin_level
        self.id = id_token
        self.id_group = id_group

    def save_in_db(self):

        if self.id == -1:

            with db_connection.get_cursor() as cursor:
                cursor.execute(q.insert_token, (self.id_group, self.text, self.is_admin, self.admin_level))
                print(cursor.fetchall())
                cursor.execute("SELECT MAX(`ID_RegisterToken`) FROM `RegisterToken`")
                self.id = cursor.fetchone()[0]
                db_connection.connection.commit()
        else:
            print('token is already saved in database')

    def delete_from_db(self):
        with db_connection.get_cursor() as cursor:
            cursor.execute(q.delete_token, (self.text,))
            print(cursor.fetchall())
            self.id = -1
            db_connection.connection.commit()

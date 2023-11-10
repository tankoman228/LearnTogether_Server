import hashlib
import password_hash
import db_connection
import Queries.QueryStrings as q


class Token:

    #select from
    def __init__(self, id_group, hash, is_admin, admin_level, id_token):
        self.hash = hash
        self.is_admin = is_admin
        self.admin_level = admin_level
        self.id = id_token
        self.id_group = id_group

    #insert into
    def __init__(self, id_group, text, is_admin, admin_level=0):
        self.hash = password_hash.hash_password(text)
        self.is_admin = is_admin
        self.admin_level = admin_level
        self.id = -1
        self.id_group = id_group

    def save_to_db(self, id_group: int):

        if self.id is -1:

            self.id_group = id_group

            with db_connection.get_cursor() as cursor:
                cursor.execute(q.insert_token, (id_group, self.hash, self.is_admin, self.admin_level))
                print(cursor.fetchall())
                cursor.execute("SELECT MAX(`ID_RegisterToken`) FROM `RegisterToken`")
                self.id = cursor.fetchone()[0]
                db_connection.connection.commit()
        else:
            print('token is already saved in database')

    def delete_from_db(self):
        with db_connection.get_cursor() as cursor:
            cursor.execute(q.delete_token, (self.hash,))
            print(cursor.fetchall())
            self.id = -1
            db_connection.connection.commit()

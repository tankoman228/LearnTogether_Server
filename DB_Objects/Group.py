import DB_Queries.QueryStrings as q
import db_connection


class Group:
    def __init__(self, name, description=None, icon=None, id_group=-1):
        self.name = name
        self.description = description
        self.icon = icon
        self.id = id_group
        self.icon_changed = False

    def save_in_db(self):

        if self.id == -1:
            with db_connection.get_cursor() as cursor:
                cursor.execute(q.insert_group, (self.name, self.description))
                print(cursor.fetchall())
                cursor.execute("SELECT MAX(`ID_Group`) FROM `Group`")
                self.id = cursor.fetchone()[0]
                db_connection.connection.commit()
        else:
            with db_connection.get_cursor() as cursor:
                cursor.execute(q.update_group, (self.name, self.description, self.id))
                print(cursor.fetchall())
                if self.icon_changed:
                    cursor.execute(q.update_group_icon, (self.icon, self.id))
                    print("Update Group Icon!", cursor.fetchall())
                db_connection.connection.commit()

    def delete_from_db(self):

        with db_connection.get_cursor() as cursor:
            cursor.execute(q.delete_group, (self.id,))
            print(cursor.fetchall())
            db_connection.connection.commit()
        self.id = -1

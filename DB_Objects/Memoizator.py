from DB_Objects.Group import Group
from DB_Objects.Token import Token
import db_connection


class Memoizator:

    def __init__(self, typename: type):

        self.__memorized = []
        print("loading to Memoizator from DB")

        if typename == Group:
            with db_connection.get_cursor() as cursor:
                cursor.execute('SELECT * FROM `Group`')

                rows = cursor.fetchall()

                for row in rows:
                    self.__memorized.append(Group(row[1], row[3], row[2], row[0]))
                print(len(self.__memorized), " groups")

        elif typename == Token:

            with db_connection.get_cursor() as cursor:

                cursor.execute('SELECT * FROM `RegisterToken`')
                rows = cursor.fetchall()
                for row in rows:
                    self.__memorized.append(Token(row[1], row[2], row[3], row[4], row[0]))
                print(len(self.__memorized), " tokens")
        else:
            raise Exception('Error: unknown type for Memorization')

    def get_by_id(self, i: int):
        for obj in self.__memorized:
            if obj.id == i:
                return obj

        print("Memoizator error: id not found")
        return None

    def find_by_name(self, name: str):
        for obj in self.__memorized:
            if obj.name == name:
                return obj

        print("Memoizator error: name not found")
        return None

    def search(self, params: [], count, id_lesser_than=2147483645):

        found = []

        try:

            for obj in self.__memorized:

                if obj.id > id_lesser_than:
                    continue

                coincidences = False
                if len(params) == 0:
                    coincidences = True

                for param in params:
                    if obj.name.find(param):
                        coincidences = True
                        break
                    else:
                        for tag in obj.tags:
                            if tag.find(param):
                                coincidences = True
                                break

                if coincidences:
                    found.append(obj)
                    if len(found) >= count:
                        return found

            return found
        except:
            print("Error: can't search in this list")

    def delete(self, obj):
        obj.delete_from_db()
        self.__memorized.remove(obj)

    def save(self, obj):
        obj.save_in_db()
        if obj not in self.__memorized:
            self.__memorized.append(obj)


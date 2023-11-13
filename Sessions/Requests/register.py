from DB_Objects.Account import Account
import db_connection

def register(account: Account, token, username, password, contact, title):

    with db_connection.connection.cursor() as cursor:

        cursor.execute("SELECT * FROM ...")

        result = cursor.fetchall()
        print(result)

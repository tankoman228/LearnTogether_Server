import db_connection
import password_hash
from DB_Objects.Account import Account
from API.Session import Session


def login(session: Session, username, password):
    with db_connection.connection.cursor() as cursor:

        cursor.execute("SELECT * FROM `Account` WHERE `Username` = %s", username)
        result = cursor.fetchone()

        if result is None:
            session.send_data_to_user("no_user_found")
            return

        if password_hash.check_password(result[2], password):
            session.account = Account(result[1], result[2], result[3], result[4], result[5], result[6], result[7],
                                      result[8], result[9], result[10], result[0])
            session.send_data_to_user("success")

        session.send_data_to_user("wrong_password")

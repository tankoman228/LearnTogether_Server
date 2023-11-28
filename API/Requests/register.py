from API.Session import Session
import DB_Objects.Account
from DB_Objects.Account import Account
import db_connection
import password_hash


# create NEW Account only. Returns True if success, False in case of error
def register(session: Session, token: str, username: str, password: str, contact: str, title: str):
    with db_connection.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM `RegisterToken` WHERE `Text` = %s", token)
        row = cursor.fetchone()

        if row is None:
            print("Unsuccessful attempt of register. Session: ", session)
            return False

        new_acc = Account(username, password_hash.hash_password(password), contact, title, None, None, row[3], row[4],
                          0, None)

        if new_acc.save_in_db():
            cursor.execute("INSERT INTO `AccountGroup` (`ID_Group`,`ID_Account`) VALUES (%s, %s)", row[1], new_acc.id)
            db_connection.connection.commit()

            session.account = new_acc
            return True

        return False

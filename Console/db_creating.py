import db_connection

def drop_and_create(cmd):

    if (input("If you already have database, this will destroy all your data in it. "
              "You will not be able to cancel after DROP + CREATE. Print 1 to accept, print something else to decline\n") == '1'):
        f = open('Queries\\CreateDB.sql', 'r')
        SQL = f.read().split(";")
        f.close()

        with db_connection.connection.cursor() as cursor:

            errors = 0

            for sql in SQL:
                try:
                    cursor.execute(sql)
                except:
                    errors += 1

            if errors > 1:
                print("Error: query errors")

            result = cursor.fetchall()
            print(result)

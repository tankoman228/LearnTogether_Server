from sqlalchemy import text

from ServerConsole import console_executor_start

import DB
DB.connect()

accs = DB.query(text('SELECT * FROM Account'))

for acc in accs:
    print(acc.Username)

console_executor_start()


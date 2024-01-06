from sqlalchemy import text

from ServerConsole import console_executor_start

import DB
DB.connect()

accs = DB.SessionEngine.query(DB.Account).where(DB.Account.Username != 1)

for acc in accs:
    print(acc.Username)

console_executor_start()


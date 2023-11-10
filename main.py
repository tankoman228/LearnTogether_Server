import DB_Objects.Memoizator as mem
import db_connection

db_connection.open_connection()
#mem.load_all_from_db()

from Console.server_console_main import *

cmd = 'help'

while cmd != 'exit':

    cmd = input()

    try:
        if cmd.split()[0] in commands.keys():
            commands[cmd.split()[0]](cmd)
        else:
            print('''
            Unknown command, Print help to get list of existing commands
            ''')
    except:
        print("Unknown error")
        pass

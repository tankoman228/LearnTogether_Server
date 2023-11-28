import db_connection

try:
    db_connection.open_connection()
    from Console.server_console_main import *
    import API.SessionManager
except Exception as e:
    print("db loading error: ", e)

cmd = 'help'

while cmd != 'exit':

    cmd = input()

    if not cmd:
        continue

    try:
        if cmd.split()[0] in commands.keys():
            commands[cmd.split()[0]](cmd)
        else:
            print('Unknown command, Print help to get list of existing commands')
    except Exception as e:
        print("Unknown error: ", e)
        pass

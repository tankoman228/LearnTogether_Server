from Console.server_console_main import *

cmd = 'help'

while cmd != 'exit':

    try:
        if cmd.split()[0] in commands.keys():
            commands[cmd.split()[0]](cmd)
        else:
            print('''
            Unknown command, Print help to get list of existing commands
            ''')
    except:
        pass

    cmd = input()

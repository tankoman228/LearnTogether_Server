import ServerConsole.help

__console_commands = {
    'help': help.help_,
    'stats': None,
    'start': None,
    'stop': None,
    'exit': None,
    'recreate_db': None,
    'load_db': None,
    'groups': None,
    'create_group': None,
    'delete_group': None,
    'create_token': None,
    'delete_token': None,
    'delete_all_tokens': None,
    'tokens': None,
    'db_raw_query': None,
    'log': None
}


def console_executor_start():
    while True:

        cmd = input()

        if not cmd:
            continue

        cmd = cmd.split()

        if cmd[0] in __console_commands.keys():
            c = cmd.pop(0)
            __console_commands[c](cmd)
        else:
            print('Unknown command! Print help to get full list of available commands')

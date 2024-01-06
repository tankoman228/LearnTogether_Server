import DB
import ServerConsole.help
import ServerConsole.groups

__console_commands = {
    'help': help.help_,
    'stats': None,
    'start': None,
    'stop': None,
    'exit': None,
    'recreate_db': DB.recreate_db,
    'load_db': None,
    'groups': groups.groups,
    'create_group': groups.create_group,
    'delete_group': groups.delete_group,
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

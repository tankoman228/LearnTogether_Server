import DB
import ServerConsole.help
import ServerConsole.groups
import ServerConsole.stats
import ServerConsole.roles
import ServerConsole.tokens
import ServerConsole.debug
import ServerConsole.accounts
import API

__console_commands = {

    'help': help.help_,
    'stats': stats.stats_collect,
    'start': API.start,
    'stop': None,
    'exit': None,
    'recreate_db': DB.recreate_db,

    'roles': roles.roles_out,
    'create_role': roles.create_role,
    'delete_role': roles.delete_role,
    'change_permissions': roles.change_permissions,

    'groups': groups.groups,
    'create_group': groups.create_group,
    'delete_group': groups.delete_group,

    'recover': accounts.recover,

    'tokens': tokens.tokens,
    'create_token': tokens.create_token,
    'delete_token': tokens.delete_token,
    'delete_all_tokens': tokens.delete_all_tokens,

    'debug_token': debug.create_session_token,
    'debug_notification': debug.send_debug_notification
}


def console_executor_start():

    print('Starting commands from file start_commands.txt')

    f = open('start_commands.txt', 'r')
    cmds = f.read().split('\n')
    f.close()

    for cmd in cmds:
        cmd_ = cmd.split()
        if len(cmd_) == 0:
            break

        if cmd_[0] in __console_commands.keys():
            c = cmd_.pop(0)
            __console_commands[c](cmd_)
        else:
            print('Unknown command! Print help to get full list of available commands')

    print('\nAll commands from file start_commands.txt have been executed\n')

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

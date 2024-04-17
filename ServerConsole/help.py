import os


def help_(args):
    if len(args) > 0:
        if args[0] == 'full':
            full_help(None)
            return

    help_file_path = os.path.join('ServerConsole', 'Texts', 'help.txt')
    with open(help_file_path, 'r') as f:
        print(f.read())


def full_help(args):
    full_help_file_path = os.path.join('ServerConsole', 'Texts', 'full_help.txt')
    with open(full_help_file_path, 'r') as f:
        print(f.read())

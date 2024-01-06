def help_(args):

    if len(args) > 0:
        if args[0] == 'full':
            full_help(None)
            return

    f = open('ServerConsole\\Texts\\help.txt', 'r')
    print(f.read())
    f.close()


def full_help(args):
    f = open('ServerConsole\\Texts\\full_help.txt', 'r')
    print(f.read())
    f.close()
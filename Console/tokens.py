from DB_Objects.Memoizator import Memoizator
from DB_Objects.Token import Token
import Console.groups as g
import password_hash

try:
    tokens = Memoizator(Token)
except:
    pass


def create_token(cmd: str):

    args = cmd.split(' ')

    gr = g.groups.get_by_id(int(args[1]))
    if gr is None:
        print("wrong args! Cannot find group with this id")
        return

    is_admin = args[3] == '1'

    admin_level = 0
    if is_admin:
        admin_level = int(args[4])

    t = Token(
        gr.id,
        args[2],
        is_admin,
        admin_level
    )
    tokens.save(t)


def delete_token(cmd: str):

    args = cmd.split()
    if len(args) != 2:
        print("wrong args!")
        return

    tokens.delete(tokens.get_by_id(int(args[1])))


def delete_all_tokens(cmd: str):

    helper = True

    while helper:
        helper = False
        for token in tokens.search([],99999):
            tokens.delete(token)
            helper = True
            break


def tokens_info(cmd):
    for t in tokens.search([], 9999):
        print([t.id, t.is_admin, t.admin_level])

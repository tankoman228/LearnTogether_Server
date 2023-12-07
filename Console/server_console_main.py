import Console.help
import Console.db_creating
import Console.start
import Console.exit
from Console.groups import *
from Console.tokens import *

commands = {
    "help": Console.help.help_usual,
    "help+": Console.help.full_help,
    "recreate_db": Console.db_creating.drop_and_create,
    "exit": Console.exit.exit,
    "create_group": create_group,
    "groups": groups_get_all,
    "delete_group": delete_group,
    "create_token": create_token,
    "delete_token": delete_token,
    "delete_all_tokens": delete_all_tokens,
    "tokens": tokens_info
}

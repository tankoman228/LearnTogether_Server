import Console.help
import Console.db_creating
import Console.start

commands = {
    "help": Console.help.help_usual,
    "help+": Console.help.full_help,
    "recreate_db": Console.db_creating.drop_and_create,
    "start": Console.start.real_start
}

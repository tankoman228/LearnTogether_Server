import Console.help
import Console.db_creating
import Console.start
import Console.exit

commands = {
    "help": Console.help.help_usual,
    "help+": Console.help.full_help,
    "recreate_db": Console.db_creating.drop_and_create,
    "start": Console.start.real_start,
    "exit": Console.exit.exit
}

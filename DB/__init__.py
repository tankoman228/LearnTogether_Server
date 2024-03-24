import json

from sqlalchemy import create_engine, Executable, text
from sqlalchemy.orm import Session, sessionmaker

from DB.execute_from_file import executor
from DB.model import *

#  Session for work with database
Ses: Session

try:
    with open('config.json', 'r') as file:
        config = json.load(file)
except FileNotFoundError:
    raise Exception("ERROR: config.json not found!")
try:
    db_host = config['db_host']
    db_name = config['db_name']
    db_port = config['db_port']
    db_user = config['db_user']
    db_password = config['db_password']
except Exception as e:
    raise Exception("ERROR: config.json : data is not valid")


#  Connects to DBMS and trying to connect to DBMS
def connect():

    print('connection attempt ', 'db engine creating, searching for database')
    try:
        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
        Base.metadata.create_all(engine)

    except Exception as e:

        print('connection attempt ', "VALID DATABASE NOT FOUND, you can create it with script"
                                     " deprecated__CreateDB.sql or command recreate_db \n\n\n Error: ", e)

        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}")

        print('connection attempt ', 'Engine created with no connection to database')

    #
    global Ses
    Ses = Session(engine)

    print('SUCCESS')


def update_session():
    global Ses
    Ses.close()
    # Создаем новый engine и сессию
    engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Ses = Session()

    print('Session updated successfully')


#  Executes query and commits changes
def query_and_commit(sql: Executable):
    r = Ses.execute(sql)
    Ses.commit()
    return r


#  DROP IF EXISTS script start
def recreate_db(args):
    print('RECREATING DB def START')

    if input('ATTENTION! This command will run script DROP IF EXISTS that means your \n'
             'previous database will be erased, this script will create new one using \n'
             'scripts from DB\\DB_Queries\\*.sql | Print  1  to confirm ') != '1':
        print('DROP IF EXISTS script execution cancelled. Existing database won\'t be damaged')
        return

    print("\t DROP IF EXISTS SCRIPT START")
    executor("DB\\DB_Queries\\DropCreate.sql", Ses)

    print("\t RECONNECTING TO CREATED DATABASE")
    Ses.close()
    connect()

    print("\t FILLING WITH BASIC VALUES")
    executor("DB\\DB_Queries\\FillBasic.sql", Ses)

    print("\t FINISHED")

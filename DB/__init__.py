import json

from sqlalchemy import create_engine, Executable, text
from sqlalchemy.orm import Session, sessionmaker

from DB.execute_from_file import executor
from DB.model import *


# считывание данных для подключения из БД
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
    global engine
    engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    Base.metadata.create_all(engine)
    print('SUCCESS')


# Создание сессии
def create_session():
    Session = sessionmaker(bind=engine)
    return Session()


def query_and_commit(session: Session, sql: Executable):
    try:
        r = session.execute(sql)
        session.commit()
        return r
    except Exception as e:
        session.rollback()
        raise e


#  DROP IF EXISTS script start
def recreate_db(args):
    print('RECREATING DB def START')

    if input('ATTENTION! This command will run script DROP IF EXISTS that means your \n'
             'previous database will be erased, this script will create new one using \n'
             'scripts from DB\\DB_Queries\\*.sql | Print  1  to confirm ') != '1':
        print('DROP IF EXISTS script execution cancelled. Existing database won\'t be damaged')
        return

    print("\t DROP IF EXISTS SCRIPT START")
    s = create_session()
    executor("DB\\DB_Queries\\DropCreate.sql", s)
    s.close()

    print("\t RECONNECTING TO CREATED DATABASE")
    connect()

    print("\t FILLING WITH BASIC VALUES")
    s = create_session()
    executor("DB\\DB_Queries\\FillBasic.sql", s)

    print("\t FINISHED")

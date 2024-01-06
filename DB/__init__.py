import json

from sqlalchemy import create_engine, Executable
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

SessionEngine: Session


def connect():
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        raise Exception("ERROR: config.json not found!")

    print('parsing config.json')
    try:
        db_host = config['db_host']
        db_name = config['db_name']
        db_port = config['db_port']
        db_user = config['db_user']
        db_password = config['db_password']
    except Exception as e:
        raise Exception("ERROR: config.json : data is not valid")

    try:
        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    except Exception as e:
        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}")

        print("DATABASE NOT FOUND, you can create it with script CreateDB.sql or command recreate_db \n\n\n Error: ", e)

    base = automap_base()
    base.prepare(engine, reflect=True)

    global SessionEngine
    SessionEngine = Session(engine)


def query(sql: Executable):
    r = SessionEngine.execute(sql)
    SessionEngine.commit()
    return r

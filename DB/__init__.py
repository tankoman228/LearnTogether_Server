import json

from sqlalchemy import create_engine, Executable, Table, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import DB

#  Session for work with database
SessionEngine: Session

#  Classes from database
Role: None
Permission: None
Group: None
Account: None
AccountGroup: None
RegisterToken: None
Recovery: None
Tag: None
InfoBase: None
InfoTag: None
ForumAsk: None
News: None
Task: None
TaskAccount: None
Information: None
Meeting: None
MeetingRespond: None
Vote: None
VoteItem: None
VoteAccount: None
Comment: None
Complaint: None


def connect():
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

    try:
        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    except Exception as e:
        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}")

        print("DATABASE NOT FOUND, you can create it with script CreateDB.sql or command recreate_db \n\n\n Error: ", e)

    base = automap_base()
    base.prepare(engine, reflect=True)

    #  Loading classes from database
    global Role, Permission, Group, Account, AccountGroup, RegisterToken
    global Recovery, Tag, InfoBase, InfoTag, ForumAsk, News
    global Task, TaskAccount, Information, Meeting, MeetingRespond
    global Vote, VoteItem, VoteAccount, Comment, Complaint

    Role = base.classes.role
    Permission = base.classes.permission
    Group = base.classes.group
    Account = base.classes.account
    AccountGroup = base.classes.accountgroup
    RegisterToken = base.classes.registertoken
    Recovery = base.classes.recovery
    Tag = base.classes.tag
    InfoBase = base.classes.infobase
    InfoTag = base.classes.infotag
    ForumAsk = base.classes.forumask
    News = base.classes.news
    Task = base.classes.task
    TaskAccount = base.classes.taskaccount
    Information = base.classes.information
    Meeting = base.classes.meeting
    MeetingRespond = base.classes.meetingrespond
    Vote = base.classes.vote
    VoteItem = base.classes.voteitem
    VoteAccount = base.classes.voteaccount
    Comment = base.classes.comment
    Complaint = base.classes.complaint

    #
    global SessionEngine
    SessionEngine = Session(engine)


def query_and_commit(sql: Executable):
    r = SessionEngine.execute(sql)
    SessionEngine.commit()
    return r


def recreate_db(args):

    if input('ATTENTION! This command will run script DROP IF EXISTS that means your \n'
             'previous database will be erased, this script will create new one using \n'
             'script DB\\DB_Queries\\CreateDB.sql  print  1  to confirm ') != '1':
        return

    #  recreate script start
    f = open('DB\\DB_Queries\\CreateDB.sql', 'r')

    sqls = f.read().split(';')
    sqls.remove('')
    for sql in sqls:
        query_and_commit(text(sql))

    f.close()

    #
    SessionEngine.close()
    connect()

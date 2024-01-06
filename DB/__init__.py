import json

from sqlalchemy import create_engine, Executable, Table, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

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


#Connects to DBMS and trying to connect to DBMS
def connect():

    print('connection attempt start')

    print('connection attempt ', 'config.json parsing')
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

    print('connection attempt ', 'db engine creating, searching for database')
    try:
        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

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

    except Exception as e:

        print('connection attempt ', "VALID DATABASE NOT FOUND, you can create it with script"
              " CreateDB.sql or command recreate_db \n\n\n Error: ", e)

        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}")

        print('connection attempt ', 'Engine created with no connection to database')

    #
    global SessionEngine
    SessionEngine = Session(engine)


#  Executes query and commits changes
def query_and_commit(sql: Executable):
    r = SessionEngine.execute(sql)
    SessionEngine.commit()
    return r


#  DROP IF EXISTS script start
def recreate_db(args):

    print('RECREATING DB def START')

    script_file_path = 'DB\\DB_Queries\\CreateDB.sql'
    if len(args) > 0:
        script_file_path = ''
        for arg in args:
            script_file_path += arg + ' '
        print('trying to load db from other script. Path to new script is: \n', script_file_path)

    if input('ATTENTION! This command will run script DROP IF EXISTS that means your \n'
             'previous database will be erased, this script will create new one using \n'
             f'script | {script_file_path} | Print  1  to confirm ') != '1':
        print('DROP IF EXISTS script execution cancelled. Existing database wouldn\'t be damaged')
        return

    #  recreate script start
    try:
        f = open(script_file_path, 'r')
        sqls = f.read().split(';')
        f.close()

        try:
            sqls.remove('')
        except:
            pass
    except Exception as e:
        print(f'Can\'t recreate database from script: {script_file_path}. '
              f'Maybe, this file does not exists. \nError: {e}')
        return

    try:
        for sql in sqls:
            query_and_commit(text(sql))
    except Exception as e:
        print('Your SQL script contained some errors, try recreate_db using right script. Error is: \n', e)

    #
    SessionEngine.close()
    connect()

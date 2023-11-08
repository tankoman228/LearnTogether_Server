import json

import pymysql

connection: pymysql.connections.Connection


def open_connection():
    print('open connection: starting')

    try:
        with open('../config.json', 'r') as file:
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
    except:
        raise Exception("ERROR: config.json : data is not valid")

    print('Open connection')

    global connection

    connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_password,
                                 db=db_name,
                                 port=db_port)

    print('connection open: success!')


def close_connection():
    connection.close()


def get_cursor():
    return connection.cursor()

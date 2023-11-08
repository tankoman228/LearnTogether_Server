import json
import db_connection


def start():

    try:
        with open('../config.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        raise Exception("ERROR: config.json not found!")

    try:
        db_connection.db_host = config['db_host']
        db_connection.db_name = config['db_name']
        db_connection.db_port = config['db_port']
        db_connection.db_user = config['db_user']
        db_connection.db_password = config['db_password']
    except:
        raise Exception("ERROR: config.json : data is not valid")

    inp_command = input()

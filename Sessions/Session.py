from DB_Objects.Account import Account
import socket
from Sessions.Requests.requests_main import *

class Session:

    def __init__(self, con):
        self.queue = []
        self.con = con
        self.account = None

    def command(self, command: str):

        if command in request_types.keys():

            args = []

            for i in range(0, request_types[command].args_num):
                data = str(self.con.recv(2048).decode())
                args.append(data)

            request_types[command].function(self.account, args)

        else:
            print("unknown_command")
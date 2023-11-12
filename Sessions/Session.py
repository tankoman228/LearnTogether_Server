from DB_Objects.Account import Account
import socket
import Sessions.Requests.requests_main as cmd

class Session:

    def __init__(self, socket):
        self.queue = []
        self.socket = socket

    def command(self, command):
        pass

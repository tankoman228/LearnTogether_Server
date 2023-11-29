import json
from _thread import start_new_thread

from API.Requests.requests_main import request_types

class Session:

    def __init__(self, con):
        self.queue = []
        self.con = con
        self.account = None
        self.carma = 0

    def command(self, command: str):

        if command in request_types.keys():

            args = []

            command = request_types[command]
            if command.file_sender:
                args.append(self.receive_json_stream())

            for i in range(0, command.args_num):
                data = str(self.con.recv(2048).decode())
                args.append(data)

            command.function(self, args)

        else:
            print("unknown_command")
            self.carma -= 100

    def receive_json_stream(self):
        received_data = b''
        current_size = 0

        while True:
            chunk = self.con.recv(2048)
            current_size += 2048

            try:
                if ((not chunk)
                        | (current_size > 33554432)
                        | (chunk.decode() == "STOP SENDING q][weprotiuy'a;sldkfjghz/.xc,mvnbbnonvcwklscdf")):
                        break
            except:
                pass
            received_data += chunk

        print("receive_finished")
        return received_data

    def send_data_to_user(self, message):
        start_new_thread(self.__send, (message,))

    def __send(self, message):
        self.con.sendall(message.encode())

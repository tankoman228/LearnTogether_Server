import json
from _thread import start_new_thread

from API.Requests.requests_main import request_types

class Session:

    def __init__(self, con, other_sessions):
        self.queue = []
        self.con = con
        self.account = None
        self.carma = 0
        self.other_sessions = other_sessions

    def command(self, command: str):

        if command in request_types.keys():

            args = []

            command = request_types[command]
            if command.file_sender:
                print(self.receive_json_stream())

            for i in range(0, command.args_num):
                data = str(self.con.recv(2048).decode())
                print(data + '\n')
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

        if current_size > 33554432:
            raise Exception('too big file!')

        print("receive_finished")
        return received_data

    def send_data_to_user(self, message):
        start_new_thread(self.__send, (message,))
        print('send data to user: ', message)

    def __send(self, message):
        self.con.sendall(message.encode())

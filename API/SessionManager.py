import socket
from _thread import start_new_thread
from API.Session import Session

server = socket.socket()
hostname = 'localhost' #socket.gethostname()
port = 9540
max_clients = 99

server.bind((hostname, port))

server.listen(99)

sessions = []


def client_thread(con):

    ses = Session(con)
    sessions.append(ses)

    x = 0

    while True:
        try:
            data = str(con.recv(2048).decode())
            print("Socket_request: ", data)
            ses.command(data)
        except Exception as e:
            print("Session error: ", e)
            break
    sessions.remove(ses)


print("Server running")


def while_true_server():
    while True:
        client, _ = server.accept()  # принимаем клиента
        start_new_thread(client_thread, (client,))  # запускаем поток клиента


start_new_thread(while_true_server, ())

import socket
import threading
from _thread import start_new_thread
from DB_Objects.Account import Account
from Sessions.Session import Session

server = socket.socket()
hostname = socket.gethostname()
port = 91540
max_clients = 99

server.bind((hostname, port))

server.listen(99)

sessions = []


def client_thread(con):
    ses = Session(con)
    sessions.append(ses)
    try:
        data = str(con.recv(2048).decode())
        print("Socket_request: ", data)



    except Exception as e:
        print("Session error: ", e)
    sessions.remove(ses)


print("Server running")
while True:
    client, _ = server.accept()  # принимаем клиента
    start_new_thread(client_thread, (client,))  # запускаем поток клиента

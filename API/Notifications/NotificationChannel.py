import socket
import threading
import API.AuthSession

notification_port = 8001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))
server_socket.listen(120)

notification_tokens_channels = {}


class NotificationChannel:

    def __init__(self, client_socket):
        self.thread = threading.Thread(target=self.handle)
        self.thread.start()
        self.client_socket = client_socket
        self.session = None

    def handle(self):
        token = str(self.client_socket.recv(1024).decode())[0:15]

        if not token or str(token) not in API.AuthSession.auth_sessions.keys():
            return

        notification_tokens_channels[token] = self

    def send_message(self, message):
        self.client_socket.send(str(message).encode())

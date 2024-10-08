import json
import socket
import threading
import API.AuthSession

notification_port = 24999
# try:
#     with open('config.json', 'r') as file:
#         config = json.load(file)
#
#         notification_port = config["notification_port"]
#         HOST = config["local_ip"]
#
# except FileNotFoundError:
#     raise Exception("ERROR: config.json not found!")
#
#
# print(HOST, ":", notification_port)
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((HOST, notification_port))
#
# print('host: ', socket.gethostname())
# server_socket.listen(120)
#
# notification_tokens_channels = {}
#
#
# class NotificationChannel:
#
#     def __init__(self, client_socket):
#         self.client_socket = client_socket
#         self.session = None
#         self.thread = threading.Thread(target=self.handle)
#         self.thread.start()
#
#     def handle(self):
#         token = str(self.client_socket.recv(1024).decode())[0:15].replace(' ', '')
#
#         print(f'Notification_token is:')
#         print(token)
#         print(API.AuthSession.notification_keys.keys())
#
#         if token not in API.AuthSession.notification_keys.keys():
#             self.send_message("Declined")
#             print("Notification token declined!")
#             return
#         self.session = API.AuthSession.notification_keys[token]
#
#         print("Notification token accepted!")
#         notification_tokens_channels[token] = self
#
#         self.send_message("Accepted")
#
#     def send_message(self, message):
#         self.client_socket.send((str(message) + '\n').encode())

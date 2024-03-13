import json
import threading
import API.Notifications.notificationManager
import API.Notifications.NotificationChannels

from fastapi import FastAPI, Body

import API.AuthSession as AuthSession
from API.Notifications import notificationManager
import DB

api = FastAPI()


@api.post("/check_notifications")
def wenomechainsama(payload: dict = Body(...)):

    if ('session_token' not in payload.keys()) or (payload['session_token'] not in AuthSession.auth_sessions.keys()):
        return {"Error": "Unknown session"}

    session: AuthSession.AuthSession = AuthSession.auth_sessions[payload['session_token']]
    try:

        lst = notificationManager.users_ids_notification_lists[session.account.ID_Account]
        print(lst)
        notificationManager.users_ids_notification_lists[session.account.ID_Account] = []
        return {"List": lst}

    except Exception as e:
        print(e)
        return {"Error": "Unknown error"}


# try:
#     print('Notifications manager starting')
#     with open('config.json', 'r') as file:
#         config = json.load(file)
#
#     NotificationChannels.notification_port = int(config['notification_port'])
#
# except FileNotFoundError:
#     raise Exception("ERROR: config.json not found!")
# except Exception as e:
#     raise Exception("ERROR: config.json : data is not valid")
#
#
# def client_receiving_cycle():
#
#     print('Notifications manager started on port: ', NotificationChannels.notification_port)
#
#     while True:
#         new_client_channel = None
#         try:
#             client_socket, addr = NotificationChannels.server_socket.accept()
#             print(f"Connection from {addr} has been established!")
#             new_client_channel = NotificationChannels.NotificationChannel(client_socket)
#         except Exception as ee:
#             print("socket error: ", ee)
#             if new_client_channel is not None:
#                 NotificationChannels.notification_tokens_channels.popitem(new_client_channel)
#
#
# threading.Thread(target=client_receiving_cycle, args=()).start()

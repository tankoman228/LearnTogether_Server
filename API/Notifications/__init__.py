import json
import threading
import API.Notifications.notificationManager

import API.Notifications.NotificationChannel

try:
    with open('config.json', 'r') as file:
        config = json.load(file)

    NotificationChannel.notification_port = int(config['notification_port'])

except FileNotFoundError:
    raise Exception("ERROR: config.json not found!")
except Exception as e:
    raise Exception("ERROR: config.json : data is not valid")


def client_receiving_cycle():
    while True:
        new_client_channel = None
        try:
            client_socket, addr = NotificationChannel.server_socket.accept()
            print(f"Connection from {addr} has been established!")
            new_client_channel = NotificationChannel.NotificationChannel(client_socket)
        except Exception as ee:
            print("socket error: ", ee)
            if new_client_channel is not None:
                NotificationChannel.notification_tokens_channels.popitem(new_client_channel)


threading.Thread(target=client_receiving_cycle, args=())

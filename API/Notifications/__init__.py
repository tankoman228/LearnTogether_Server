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


def client_recieving_cycle():
    while True:
        try:
            client_socket, addr = NotificationChannel.server_socket.accept()
            print(f"Connection from {addr} has been established!")

            new_client = NotificationChannel.NotificationChannel(client_socket)
        except Exception as ee:
            print("socket error: ", ee)


threading.Thread(target=client_recieving_cycle, args=())

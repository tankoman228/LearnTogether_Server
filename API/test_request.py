from fastapi import FastAPI
import API.Notifications

# ППЛГОНД
api = FastAPI()


@api.post('/Test')
def index():
    return {"Success": True, "NotificationPort": API.Notifications.NotificationChannels.notification_port}

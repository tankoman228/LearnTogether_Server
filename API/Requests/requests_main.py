from API.Requests.login import *
from API.Requests.register import *
from API.Requests.debug_message import *
from API.Requests.update_icon import *

class RequestType:

    def __init__(self, args_num: int, function, file_sender=False):
        self.args_num = args_num
        self.function = function
        self.file_sender = file_sender


request_types = {
    "debug_message":    RequestType(1, debug_message),
    "login":            RequestType(2, login),
    "register":         RequestType(5, register),
    "update_icon":      RequestType(0, update_icon, True)
}

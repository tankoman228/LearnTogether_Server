from Sessions.Requests.login import *
from Sessions.Requests.register import *
from Sessions.Requests.debug_message import *

class RequestType:

    def __init__(self, args_num: int, function ):
        self.args_num = args_num
        self.function = function


request_types = {
    "debug_message": RequestType(1, debug_message)
}
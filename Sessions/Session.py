from DB_Objects.Account import Account
from threading import Thread


class Session:

    def __init__(self):
        self.queue = []
        self.started = False

    def __cycle_new_thread(self):
        pass

    def cycle_begin(self):
        self.started = True

        t = Thread(target=self.__cycle_new_thread, args=())
        t.daemon = True
        t.start()

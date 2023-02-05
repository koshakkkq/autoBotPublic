import datetime


class User:
    def __init__(self, id, firstMsg):
        self.id = id
        self.firstMsg = firstMsg
        self.vip = False
        self.vipTill = datetime.datetime.now()

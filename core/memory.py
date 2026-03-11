class Memory:
    def __init__(self):
        self.last_item = None
        self.last_location = None
        self.last_player = None
        self.chat_history = []

    def remember_item(self, item):
        self.last_item = item

    def remember_location(self, x, y, z):
        self.last_location = (x, y, z)

    def add_chat(self, msg):
        self.chat_history.append(msg)
        if len(self.chat_history) > 10:
            self.chat_history.pop(0)

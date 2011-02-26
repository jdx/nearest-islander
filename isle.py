class Isle:
    """Represents a collection of islanders"""

    def __init__(self):
        self.islanders = []

    def __getitem__(self, index):
        return self.islanders[index]

    def add_islander(self, islander):
        self.islanders.append(islander)

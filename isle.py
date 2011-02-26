class Isle:
    """Represents a collection of islanders"""

    islanders = []

    def __getitem__(self, index):
        return self.islanders[index]

    def add_islander(self, islander):
        islander.isle = self
        self.islanders.append(islander)

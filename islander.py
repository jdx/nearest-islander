class Islander:
    """Represents an individual on an island"""

    isle = None

    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

    def __repr__(self):
        return self.name

    def nearest_neighbours(self, n=1):
        return self.isle[0]

class Islander:
    """Represents an individual on an island"""

    isle = None

    left_child = None
    right_child = None

    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

    def __repr__(self):
        return self.name

    @property
    def nearest_neighbours(self, n=5):
        return self.isle.nearest_neighbour_search(self.coords, n)[1:]

class Islander:
    """Represents an individual on an island"""

    isle = None

    # used internally for the kd-tree to help searching for islanders
    left_child = None
    right_child = None

    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

    def __repr__(self):
        return self.name

    @property
    def nearest_neighbours(self, n=5):
        # return the neighbours close to the point of this islander
        # we skip the first entry since that will be this islander
        return self.isle.nearest_neighbour_search(self.coords, n)[1:]

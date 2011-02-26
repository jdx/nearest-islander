class Islander:
    """Represents an individual on an island"""

    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

    def __repr__(self):
        return "%s %s" % ( self.name, self.coords )

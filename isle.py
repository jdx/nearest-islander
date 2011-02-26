class Isle:
    """Represents a collection of islanders"""

    islanders = []

    def __getitem__(self, index):
        return self.islanders[index]

    def add_islander(self, islander):
        islander.isle = self
        self.islanders.append(islander)

    def calculate_nearest_neighbours(self, k=5, verbose=None):
        distances = {}
        for islander_a in self.islanders:
            distances = []
            for islander_b in self.islanders:
                if islander_a == islander_b:
                    continue

                # find the euclidean distance
                x = ( islander_a.coords[0] - islander_b.coords[0] ) ** 2
                y = ( islander_a.coords[1] - islander_b.coords[1] ) ** 2
                distance = x + y

                # store the distance as a tuple
                distances.append( (islander_b, distance) )

                if verbose:
                    print '%s - %s distance^2: %f' % ( islander_a, islander_b, distance )
            distances.sort(key=lambda entry:entry[1])
            islander_a.nearest_neighbours = map(lambda entry:entry[0], distances)[0:k]

import io
from islander import Islander

class Isle:
    """Represents a collection of islanders"""

    def __init__(self, islanders, verbose=None, k=5):
        self.islanders = islanders
        for islander in self.islanders:
            islander.isle = self
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

    def __getitem__(self, index):
        return self.islanders[index]

    @classmethod
    def parse_island_file(cls, island_file_path, verbose=None):
        """ Reads in an island file and outputs a new isle"""

        islanders = []
        if verbose:
            print "Reading file: %s" % island_file_path
        with io.open(island_file_path, 'r') as file:
            line = file.readline()
            while line:

                # read in the islander
                values = line.split()
                coords = ( int(values[1]), int(values[2]) )
                islander = Islander( values[0], coords )
                islanders.append(islander)

                if verbose:
                    print 'Got islander: %s at %s' % ( islander, islander.coords )

                line = file.readline()
        isle = Isle(islanders, verbose=verbose)
        return isle

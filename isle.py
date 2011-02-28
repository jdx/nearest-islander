import io
from islander import Islander

class Isle:
    """Represents a collection of islanders. Some code based off of http://code.google.com/p/python-kdtree/"""

    def __init__(self, islanders, verbose=False):
        self.islanders = islanders
        for islander in self.islanders:
            islander.isle = self
        self._root = self._build_tree(self.islanders)

    def __getitem__(self, index):
        return self.islanders[index]

    def nearest_neighbour_search(self, query_point, n=1):
        return self._nearest_neighbour_search(self._root, query_point, n, 0, Isle.IslandNeighbours(query_point, n))

    def _nearest_neighbour_search(self, islander, query_point, n, depth, best_neighbours):
        if islander == None:
            return best_neighbours

        if islander.left_child == None and islander.right_child == None:
            best_neighbours.add(islander)
            return best_neighbours

        axis = depth % 2

        near_subtree = None
        far_subtree = None
        if query_point[axis] < islander.coords[axis]:
            near_subtree = islander.left_child
            far_subtree = islander.right_child
        else:
            near_subtree = islander.right_child
            far_subtree = islander.left_child

        self._nearest_neighbour_search(near_subtree, query_point, n, depth=depth+1, best_neighbours=best_neighbours)

        best_neighbours.add(islander)

        if (islander.coords[axis] - query_point[axis])**2 < best_neighbours.largest_distance_squared:
            self._nearest_neighbour_search(far_subtree, query_point, n, depth=depth+1, best_neighbours=best_neighbours)

        return best_neighbours

    def _build_tree(self, islanders, depth=0):
        """Builds a kd-tree for the islanders. Based on code from http://en.wikipedia.org/wiki/Kd-tree"""

        if not islanders:
            return

        # pick either x or y axis
        axis = depth % 2

        # sort on the axis, then pick pivot point (median)
        islanders.sort(key=lambda islander: islander.coords[axis])
        median = len(islanders) // 2

        islander = islanders[median]
        islander.left_child = self._build_tree(islanders[0:median], depth + 1)
        islander.right_child = self._build_tree(islanders[median+1:], depth + 1)
        return islander

    @classmethod
    def parse_island_file(cls, island_file_path, verbose=False):
        """ Reads in an island file and outputs a new isle"""

        islanders = []
        if verbose:
            print "Reading file: %s" % island_file_path

        with io.open(island_file_path, 'r') as file:
            for line in file:
                values = line.split()
                coords = ( int(values[1]), int(values[2]) )
                islander = Islander( values[0], coords )
                islanders.append(islander)
                if verbose:
                    print 'Got islander: %s at %s' % ( islander, islander.coords )

        isle = Isle(islanders, verbose=verbose)
        return isle

    class IslandNeighbours():
        def __init__(self, query_point, n=5):
            self.query_point = query_point
            self.n = n
            self.largest_distance_squared = 0
            self.current_best = []

        def __getitem__(self, index):
            return map((lambda item: item[0]), self.current_best[index])

        def calculate_largest(self):
            if self.n >= len(self.current_best):
                self.largest_distance_squared = self.current_best[-1][1]
            else:
                self.largest_distance_squared = self.current_best[self.n-1][1]

        def add(self, islander):
            distance = self.__square_distance__(islander.coords, self.query_point)
            for i, e in enumerate(self.current_best):
                if i == self.n:
                    # this islander is farther away than the 5 best so far, discard
                    return
                elif e[1] > distance:
                    # this islander is closer than the current bests, insert
                    self.current_best.insert(i, (islander, distance))
                    self.calculate_largest()
                    return
            # room for more, append to the end
            self.current_best.append((islander, distance))
            self.calculate_largest()

        @staticmethod
        def __square_distance__(point_a, point_b):
            """Gets the distance between the 2 points, squared"""
            x_distance = (point_a[0] - point_b[0]) ** 2
            y_distance = (point_a[1] - point_b[1]) ** 2
            return x_distance + y_distance


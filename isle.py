import io
from islander import Islander

class Isle:
    """Represents a collection of islanders"""
    # NOTE: Some of this code is based off of http://code.google.com/p/python-kdtree/

    def __init__(self, islanders, verbose=False):
        # Grab the islanders and set the isle to this isle
        self.islanders = islanders
        for islander in self.islanders:
            islander.isle = self

        # Build the kd-tree needed to find islanders near a point
        self._root = self._build_tree(self.islanders)

    def __getitem__(self, index):
        """Gets the islanders of this isle in arbitrary order"""
        return self.islanders[index]

    def nearest_neighbor_search(self, query_point, n=1):
        """Gets n neighbors next to the query_point coordinates"""
        return self._nearest_neighbor_search(self._root, query_point, n, 0, Isle.IslandNeighbors(query_point, n))

    def _nearest_neighbor_search(self, islander, query_point, n, depth, best_neighbors):
        """Internal recursive searching for neighbors"""

        # This method finds good candidates for neighbors, then stores them in the best_neighbors structure.
        # The best_neighbors structure is smart enough to not allow you to insert neighbors that aren't as good as those already in it

        # Base case 1: Node is nothing, do nothing
        if islander == None:
            return best_neighbors

        # Base case: Node is leaf, try and insert it into best_neighbors
        if islander.left_child == None and islander.right_child == None:
            best_neighbors.add(islander)
            return best_neighbors

        # Flip the axis based on current depth
        axis = depth % 2

        # Find out what side of the tree is more likely to yield close neighbors
        near_subtree = None
        far_subtree = None
        if query_point[axis] < islander.coords[axis]:
            near_subtree = islander.left_child
            far_subtree = islander.right_child
        else:
            near_subtree = islander.right_child
            far_subtree = islander.left_child

        # Recurse down the more likely side of the kd-tree
        self._nearest_neighbor_search(near_subtree, query_point, n, depth=depth+1, best_neighbors=best_neighbors)

        # Now add the current node
        best_neighbors.add(islander)

        # If it is possible the far_subtree could have close neighbors, recurse down that side as well
        if (islander.coords[axis] - query_point[axis])**2 < best_neighbors.largest_distance_squared:
            self._nearest_neighbor_search(far_subtree, query_point, n, depth=depth+1, best_neighbors=best_neighbors)

        return best_neighbors

    def _build_tree(self, islanders, depth=0):
        """Builds a kd-tree for the islanders"""
        # Based on code from http://en.wikipedia.org/wiki/Kd-tree

        if not islanders:
            return

        # pick either x or y axis
        axis = depth % 2

        # sort on the axis, then pick pivot point (median)
        islanders.sort(key=lambda islander: islander.coords[axis])
        median = len(islanders) // 2

        # grab the root and recurse on its leaves
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
                # A line looks like this: "Bobo 2 5"
                values = line.split()
                coords = ( int(values[1]), int(values[2]) )
                islander = Islander( values[0], coords )
                islanders.append(islander)
                if verbose:
                    print 'Got islander: %s at %s' % ( islander, islander.coords )

        isle = Isle(islanders, verbose=verbose)
        return isle

    class IslandNeighbors():
        """ This class is used internally by an isle on searching to find close neighbors"""

        def __init__(self, query_point, n=5):
            self.query_point = query_point
            self.n = n
            self.largest_distance_squared = 0
            self.current_best = []

        def __getitem__(self, index):
            """Gets the islanders in order of closest to the point to furthest"""
            # Since the current_best array is tuples of the islander and its distance to the query_point,
            # we use map to return just the islander
            return map((lambda item: item[0]), self.current_best[index])

        def calculate_largest(self):
            """This stores the current largest point from the query_point"""
            if self.n >= len(self.current_best):
                self.largest_distance_squared = self.current_best[-1][1]
            else:
                self.largest_distance_squared = self.current_best[self.n-1][1]

        def add(self, islander):
            """Attempts to add an islander to the current_best list"""

            # Find out how far away the new islander is
            distance = self.__square_distance__(islander.coords, self.query_point)

            # Compare this islander to each one already in the list
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


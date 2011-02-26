import io

from isle import Isle
from islander import Islander

def parse_island_file(island_file_path, verbose=None):
    isle = Isle()

    if verbose:
        print "Reading file: %s" % island_file_path
    with io.open(island_file_path, 'r') as file:
        line = file.readline()
        while line:

            # read in the islander
            values = line.split()
            coords = ( int(values[1]), int(values[2]) )
            islander = Islander( values[0], coords )
            isle.add_islander(islander)

            if verbose:
                print 'Got islander: %s' % islander

            line = file.readline()
    return isle

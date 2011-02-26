import io

from islander import Islander

def parse_island_file(island_file_path, verbose=None):
    islanders = []

    if verbose:
        print "Reading file: %s" % island_file_path
    with io.open(island_file_path, 'r') as file:
        line = file.readline()
        while line:
            values = line.split()
            coords = ( int(values[1]), int(values[2]) )
            islander = Islander( values[0], coords )
            islanders.append(islander)
            if verbose:
                print 'Got islander: %s' % islander
            line = file.readline()
    return islanders

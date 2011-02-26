import io

def parse_island_file(island_file_path, verbose=None):
    islanders = {}

    if verbose:
        print "Reading file: %s" % island_file_path
    with io.open(island_file_path, 'r') as file:
        line = file.readline()
        while line:
            values = line.split()
            islanders[values[0]] = (int(values[1]), int(values[2]))
            if verbose:
                print 'Got islander \'%s\' at %s' % (values[0], islanders[values[0]])
            line = file.readline()
    return islanders

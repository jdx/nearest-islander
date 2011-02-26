import io

def parse_island_file(island_file_path, verbose=None):
    if verbose:
        print "Reading file: %s" % island_file_path
    with io.open(island_file_path, 'r') as file:
        line = file.readline()
        while line:
            if verbose:
                print 'parsing line: %s' % line.rstrip()
            line = file.readline()

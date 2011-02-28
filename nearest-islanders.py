from optparse import OptionParser
from isle import Isle

def main():
    usage = "usage: %prog inputfile"
    parser = OptionParser(usage=usage, version="%prog 1.0")
    parser.add_option('-v', '--verbose', action="store_true", dest="verbose")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("Must give path to input file")
        return
    elif len(args) > 1:
        parser.error("Too many arguments given")
        return
    islanders = Isle.parse_island_file(args[0], verbose=options.verbose)
    for islander in islanders:
        print "%s %s" % (islander, ','.join(map(str, islander.nearest_neighbors)))

if __name__ == "__main__":
    main()

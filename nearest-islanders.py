from optparse import OptionParser
from island_file_parser import parse_island_file

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
    islanders = parse_island_file(args[0], verbose=options.verbose)
    for islander in islanders:
        print "%s %s" % (islander, islander.nearest_neighbours(1))

if __name__ == "__main__":
    main()

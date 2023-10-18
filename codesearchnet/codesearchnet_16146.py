def main():
    """Main function."""

    # define a command-line argument parser
    description = 'Validate a CSV data file.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('file', 
                        metavar='FILE', 
                        help='a file to be validated')
    parser.add_argument('-l', '--limit',
                        dest='limit',
                        type=int,
                        action='store',
                        default=0,
                        help='limit the number of problems reported'
                        )
    parser.add_argument('-s', '--summarize',
                        dest='summarize',
                        action='store_true',
                        default=False,
                        help='output only a summary of the different types of problem found'
                        )
    parser.add_argument('-e', '--report-unexpected-exceptions',
                        dest='report_unexpected_exceptions',
                        action='store_true',
                        default=False,
                        help='report any unexpected exceptions as problems'
                        )
    
    # parse arguments
    args = parser.parse_args()
    
    # sanity check arguments
    if not os.path.isfile(args.file):
        print '%s is not a file' % args.file
        sys.exit(1)

    with open(args.file, 'r') as f:

        # set up a csv reader for the data
        data = csv.reader(f, delimiter='\t')
        
        # create a validator
        validator = create_validator()
        
        # validate the data from the csv reader
        # N.B., validate() returns a list of problems;
        # if you expect a large number of problems, use ivalidate() instead
        # of validate(), but bear in mind that ivalidate() returns an iterator
        # so there is no len()
        problems = validator.validate(data, 
                                      summarize=args.summarize,
                                      report_unexpected_exceptions=args.report_unexpected_exceptions,
                                      context={'file': args.file})

        # write problems to stdout as restructured text
        write_problems(problems, sys.stdout, 
                       summarize=args.summarize, 
                       limit=args.limit)
        
        # decide how to exit
        if problems: # will not work with ivalidate() because it returns an iterator
            sys.exit(1)
        else:
            sys.exit(0)
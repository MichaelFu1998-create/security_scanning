def parse_arguments(args):
    '''Parse arguments from the command line'''
    parser = argparse.ArgumentParser(description='Convert JAMS to .lab files')

    parser.add_argument('-c',
                        '--comma-separated',
                        dest='csv',
                        action='store_true',
                        default=False,
                        help='Output in .csv instead of .lab')

    parser.add_argument('--comment', dest='comment_char', type=str, default='#',
                        help='Comment character')

    parser.add_argument('-n',
                        '--namespace',
                        dest='namespaces',
                        nargs='+',
                        default=['.*'],
                        help='One or more namespaces to output.  Default is all.')

    parser.add_argument('jams_file',
                        help='Path to the input jams file')

    parser.add_argument('output_prefix', help='Prefix for output files')

    return vars(parser.parse_args(args))
def _parse_args(args):
    """Setup argparser to process arguments and generate help"""

    # parser uses custom usage string, with 'usage: ' removed, as it is
    # added automatically via argparser.
    parser = argparse.ArgumentParser(description="Remove and/or rearrange "
                                     + "sections from each line of a file(s).",
                                     usage=_usage()[len('usage: '):])
    parser.add_argument('-b', "--bytes", action='store', type=lst, default=[],
                        help="Bytes to select")
    parser.add_argument('-c', "--chars", action='store', type=lst, default=[],
                        help="Character to select")
    parser.add_argument('-f', "--fields", action='store', type=lst, default=[],
                        help="Fields to select")
    parser.add_argument('-d', "--delimiter", action='store', default="\t",
                        help="Sets field delimiter(default is TAB)")
    parser.add_argument('-e', "--regex", action='store_true',
                        help='Enable regular expressions to be used as input '+
                        'delimiter')
    parser.add_argument('-s', '--skip', action='store_true',
                        help="Skip lines that do not contain input delimiter.")
    parser.add_argument('-S', "--separator", action='store', default="\t",
                        help="Sets field separator for output.")
    parser.add_argument('file', nargs='*', default="-",
                        help="File(s) to cut")

    return parser.parse_args(args)
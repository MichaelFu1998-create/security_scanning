def run():
    """Main entrypoint if invoked via the command line."""
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            'Text mode diagrams using UTF-8 characters and fancy colors.'
        ),
        epilog="""
    (1): only works for the horizontal bar graph, the first argument is the key
    and the second value is the data point.
""",
    )

    group = parser.add_argument_group('optional drawing mode')
    group.add_argument(
        '-G', '--graph',
        dest='mode', action='store_const', const='g',
        help='axis drawing mode (default)',
    )
    group.add_argument(
        '-H', '--horizontal-bars',
        dest='mode', action='store_const', const='h',
        help='horizontal drawing mode',
    )
    group.add_argument(
        '-V', '--vertical-bars',
        dest='mode', action='store_const', const='v',
        help='vertical drawing mode',
    )

    group = parser.add_argument_group('optional drawing arguments')
    group.add_argument(
        '-a', '--axis',
        dest='axis', action='store_const', const=True, default=True,
        help='draw axis (default: yes)',
    )
    group.add_argument(
        '-A', '--no-axis',
        dest='axis', action='store_const', const=False,
        help="don't draw axis",
    )
    group.add_argument(
        '-c', '--color',
        dest='color', action='store_const', const=True, default=True,
        help='use colors (default: yes)',
    )
    group.add_argument(
        '-C', '--no-color',
        dest='color', action='store_const', const=False,
        help="don't use colors",
    )
    group.add_argument(
        '-l', '--legend',
        dest='legend', action='store_const', const=True, default=True,
        help='draw y-axis legend (default: yes)',
    )
    group.add_argument(
        '-L', '--no-legend',
        dest='legend', action='store_const', const=False,
        help="don't draw y-axis legend",
    )
    group.add_argument(
        '-f', '--function',
        default=None, metavar='function',
        help='curve manipulation function, use "help" for a list',
    )
    group.add_argument(
        '-p', '--palette',
        default='default', metavar='palette',
        help='palette name, use "help" for a list',
    )
    group.add_argument(
        '-x', '--width',
        default=0, type=int, metavar='characters',
        help='drawing width (default: auto)',
    )
    group.add_argument(
        '-y', '--height',
        default=0, type=int, metavar='characters',
        help='drawing height (default: auto)',
    )
    group.add_argument(
        '-r', '--reverse',
        default=False, action='store_true',
        help='reverse draw graph',
    )
    group.add_argument(
        '--sort-by-column',
        default=0, type=int, metavar='index',
        help='sort input data based on given column',
    )

    group = parser.add_argument_group('optional input and output arguments')
    group.add_argument(
        '-b', '--batch',
        default=False, action='store_true',
        help='batch mode (default: no)',
    )
    group.add_argument(
        '-k', '--keys',
        default=False, action='store_true',
        help='input are key-value pairs (default: no) (1)',
    )
    group.add_argument(
        '-s', '--sleep',
        default=0, type=float,
        help='batch poll sleep time (default: none)',
    )
    group.add_argument(
        '-i', '--input',
        default='-', metavar='file',
        help='input file (default: stdin)',
    )
    group.add_argument(
        '-o', '--output',
        default='-', metavar='file',
        help='output file (default: stdout)',
    )
    group.add_argument(
        '-e', '--encoding',
        dest='encoding', default='',
        help='output encoding (default: auto)',
    )

    option = parser.parse_args()

    if option.function == 'help':
        return usage_function(parser)

    if option.palette == 'help':
        return usage_palette(parser)

    option.mode = option.mode or 'g'
    option.size = Point((option.width, option.height))

    if option.input in ['-', 'stdin']:
        istream = sys.stdin
    else:
        istream = open(option.input, 'r')

    if option.output in ['-', 'stdout']:
        try:
            ostream = sys.stdout.buffer
        except AttributeError:
            ostream = sys.stdout
    else:
        ostream = open(option.output, 'wb')

    option.encoding = option.encoding or Terminal().encoding

    if option.mode == 'g':
        engine = AxisGraph(option.size, option)

    elif option.mode == 'h':
        engine = HorizontalBarGraph(option.size, option)

    elif option.mode == 'v':
        engine = VerticalBarGraph(option.size, option)

    else:
        parser.error('invalid mode')
        return 1

    engine.consume(istream, ostream, batch=option.batch)
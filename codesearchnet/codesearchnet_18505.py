def run_get_percentage():
    """
    Calculate what percentage a given number is of another,
    e.g. 50 is 50% of 100.
    """
    description = run_get_percentage.__doc__
    parser = argparse.ArgumentParser(
        prog='get_percentage',
        description=description,
        epilog="Example use: get_percentage 25 100",
    )
    parser.add_argument(
        'a', help='Integer or floating point number that is a percent of another number'
    )
    parser.add_argument(
        'b',
        help='Integer or floating point number of which the first number is a percent',
    )
    args = parser.parse_args()
    print(sm.get_percentage(float(args.a), float(args.b)))
def get_parser():
    """
    Generate an appropriate parser.

    :returns: an argument parser
    :rtype: `ArgumentParser`
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "package",
        choices=arg_map.keys(),
        help="designates the package to test")
    parser.add_argument("--ignore", help="ignore these files")
    return parser
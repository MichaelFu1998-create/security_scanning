def sep1(parser, separator):
    """Like sep but must consume at least one of parser.
    """
    first = [parser()]
    def inner():
        separator()
        return parser()
    return first + many(tri(inner))
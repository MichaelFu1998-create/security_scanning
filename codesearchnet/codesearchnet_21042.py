def chain(*args):
    """Runs a series of parsers in sequence passing the result of each parser to the next.
    The result of the last parser is returned.
    """
    def chain_block(*args, **kwargs):
        v = args[0](*args, **kwargs)
        for p in args[1:]:
            v = p(v)
        return v
    return chain_block
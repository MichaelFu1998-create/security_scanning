def parse_litezip(path):
    """Parse a litezip file structure to a data structure given the path
    to the litezip directory.

    """
    struct = [parse_collection(path)]
    struct.extend([parse_module(x) for x in path.iterdir()
                   if x.is_dir() and x.name.startswith('m')])
    return tuple(sorted(struct))
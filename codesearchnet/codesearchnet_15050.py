def compile_glob(spec):
    """Convert the given glob `spec` to a compiled regex."""
    parsed = "".join(parse_glob(spec))
    regex = "^{0}$".format(parsed)
    return re.compile(regex)
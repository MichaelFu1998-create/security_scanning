def parse_glob(pattern):
    """Generate parts of regex transformed from glob pattern."""
    if not pattern:
        return

    bits = pattern.split("/")
    dirs, filename = bits[:-1], bits[-1]

    for dirname in dirs:
        if dirname == "**":
            yield  "(|.+/)"
        else:
            yield glob2re(dirname) + "/"

    yield glob2re(filename)
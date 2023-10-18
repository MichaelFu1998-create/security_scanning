def clean(options, info):
    """Clean up extra files littering the source tree.

    options.paved.clean.dirs: directories to search recursively
    options.paved.clean.patterns: patterns to search for and remove
    """
    info("Cleaning patterns %s", options.paved.clean.patterns)
    for wd in options.paved.clean.dirs:
        info("Cleaning in %s", wd)
        for p in options.paved.clean.patterns:
            for f in wd.walkfiles(p):
                f.remove()
def find_standard_sakefile(settings):
    """Returns the filename of the appropriate sakefile"""
    error = settings["error"]
    if settings["customsake"]:
        custom = settings["customsake"]
        if not os.path.isfile(custom):
            error("Specified sakefile '{}' doesn't exist", custom)
            sys.exit(1)
        return custom
    # no custom specified, going over defaults in order
    for name in ["Sakefile", "Sakefile.yaml", "Sakefile.yml"]:
        if os.path.isfile(name):
            return name
    error("Error: there is no Sakefile to read")
    sys.exit(1)
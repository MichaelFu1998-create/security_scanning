def get_driver_options():
    """
    Interpret env var as key=value
    :return:
    """
    options = os.environ.get("SHOEBOT_GRAPHICS")
    if not options:
        return {}

    try:
        return dict([kv.split('=') for kv in options.split()])
    except ValueError:
        sys.stderr.write("Bad option format.\n")
        sys.stderr.write("Environment variable should be in the format key=value separated by spaces.\n\n")
        sys.stderr.write("SHOEBOT_GRAPHICS='cairo=cairocffi,cairo gi=pgi'\n")
        sys.exit(1)
def check_write_permissions(file):
    """
    Check if we can write to the given file

    Otherwise since we might detach the process to run in the background
    we might never find out that writing failed and get an ugly
    exit message on startup. For example:
    ERROR: Child exited immediately with non-zero exit code 127

    So we catch this error upfront and print a nicer error message
    with a hint on how to fix it.
    """
    try:
        open(file, 'a')
    except IOError:
        print("Can't open file {}. "
              "Please grant write permissions or change the path in your config".format(file))
        sys.exit(1)
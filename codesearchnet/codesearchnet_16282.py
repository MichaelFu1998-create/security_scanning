def get_print_functions(settings):
    """
    This returns the appropriate print functions
    in a tuple
    The print function are:
        - sprint - for standard printing
        - warn - for warnings
        - error - for errors
    This will all be the same if color is False.

    The returned print functions will contain an optional parameter
    that specifies the output level (verbose or not). If not verbose,
    the print function will ignore the message.
    """
    verbose = settings["verbose"]
    # the regular print doesn't use color by default
    # (even if color is True)
    def sprint(message, level=None, color=False):
        if level=="verbose" and not verbose:
            return
        # for colors
        prepend = ""
        postfix = ""
        if settings["color"] and color:
            prepend = "\033[92m"
            postfix = "\033[0m"
        print("{}{}{}".format(prepend, message, postfix))
        sys.stdout.flush()
    def warn(message, level=None, color=True):
        if level=="verbose" and not verbose:
            return
        # for colors
        prepend = ""
        postfix = ""
        if settings["color"] and color:
            prepend = "\033[93m"
            postfix = "\033[0m"
        print("{}{}{}".format(prepend, message, postfix))
        sys.stdout.flush()
    def error(message, level=None, color=True):
        # this condition does really make any sense but w/e
        if level=="verbose" and not verbose:
            return
        # for colors
        prepend = ""
        postfix = ""
        if settings["color"] and color:
            prepend = "\033[91m"
            postfix = "\033[0m"
        print("{}{}{}".format(prepend, message, postfix), file=sys.stderr)
        sys.stderr.flush()
    return sprint, warn, error
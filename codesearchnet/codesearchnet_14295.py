def main(argv=None):
    """The edx_lint command entry point."""
    if argv is None:
        argv = sys.argv[1:]

    if not argv or argv[0] == "help":
        show_help()
        return 0
    elif argv[0] == "check":
        return check_main(argv[1:])
    elif argv[0] == "list":
        return list_main(argv[1:])
    elif argv[0] == "write":
        return write_main(argv[1:])
    else:
        print(u"Don't understand {!r}".format(" ".join(argv)))
        show_help()
        return 1
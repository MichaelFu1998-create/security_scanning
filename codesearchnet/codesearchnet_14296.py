def show_help():
    """Print the help string for the edx_lint command."""
    print("""\
Manage local config files from masters in edx_lint.

Commands:
""")
    for cmd in [write_main, check_main, list_main]:
        print(cmd.__doc__.lstrip("\n"))
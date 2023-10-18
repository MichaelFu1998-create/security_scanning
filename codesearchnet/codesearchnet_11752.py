def _easy_install(argv, python_cmd, use_sudo):
    """
    Install packages using easy_install

    We don't know if the easy_install command in the path will be the
    right one, so we use the setuptools entry point to call the script's
    main function ourselves.
    """
    command = """python -c "\
        from pkg_resources import load_entry_point;\
        ez = load_entry_point('setuptools', 'console_scripts', 'easy_install');\
        ez(argv=%(argv)r)\
    """ % locals()
    if use_sudo:
        run_as_root(command)
    else:
        run(command)
def command_list():
    """
    Get sub-command list

    .. note::

        Don't use logger handle this function errors.

        Because the error should be a code error,not runtime error.


    :return: `list` matched sub-parser
    """
    from cliez.conf import COMPONENT_ROOT

    root = COMPONENT_ROOT

    if root is None:
        sys.stderr.write("cliez.conf.COMPONENT_ROOT not set.\n")
        sys.exit(2)
        pass

    if not os.path.exists(root):
        sys.stderr.write(
            "please set a valid path for `cliez.conf.COMPONENT_ROOT`\n")
        sys.exit(2)
        pass

    try:
        path = os.listdir(os.path.join(root, 'components'))
        return [f[:-3] for f in path if
                f.endswith('.py') and f != '__init__.py']
    except FileNotFoundError:
        return []
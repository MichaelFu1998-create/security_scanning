def append_arguments(klass, sub_parsers, default_epilog, general_arguments):
    """
    Add class options to argparser options.

    :param cliez.component.Component klass: subclass of Component
    :param Namespace sub_parsers:
    :param str default_epilog: default_epilog
    :param list general_arguments: global options, defined by user
    :return: Namespace subparser
    """

    entry_name = hump_to_underscore(klass.__name__).replace(
        '_component',
        '')

    # set sub command document
    epilog = default_epilog if default_epilog \
        else 'This tool generate by `cliez` ' \
             'https://www.github.com/wangwenpei/cliez'

    sub_parser = sub_parsers.add_parser(entry_name, help=klass.__doc__,
                                        epilog=epilog)
    sub_parser.description = klass.add_arguments.__doc__

    # add slot arguments
    if hasattr(klass, 'add_slot_args'):
        slot_args = klass.add_slot_args() or []
        for v in slot_args:
            sub_parser.add_argument(*v[0], **v[1])
        sub_parser.description = klass.add_slot_args.__doc__
        pass

    user_arguments = klass.add_arguments() or []

    for v in user_arguments:
        sub_parser.add_argument(*v[0], **v[1])

    if not klass.exclude_global_option:
        for v in general_arguments:
            sub_parser.add_argument(*v[0], **v[1])

    return sub_parser
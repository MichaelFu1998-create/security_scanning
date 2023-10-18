def get_arg_parser(cls, settings = None, option_prefix = u'--',
                                                            add_help = False):
        """Make a command-line option parser.

        The returned parser may be used as a parent parser for application
        argument parser.

        :Parameters:
            - `settings`: list of PyXMPP2 settings to consider. By default
              all 'basic' settings are provided.
            - `option_prefix`: custom prefix for PyXMPP2 options. E.g.
              ``'--xmpp'`` to differentiate them from not xmpp-related
              application options.
            - `add_help`: when `True` a '--help' option will be included
              (probably already added in the application parser object)
        :Types:
            - `settings`: list of `unicode`
            - `option_prefix`: `str`
            - `add_help`:

        :return: an argument parser object.
        :returntype: :std:`argparse.ArgumentParser`
        """
        # pylint: disable-msg=R0914,R0912
        parser = argparse.ArgumentParser(add_help = add_help,
                                            prefix_chars = option_prefix[0])
        if settings is None:
            settings = cls.list_all(basic = True)

        if sys.version_info.major < 3:
            # pylint: disable-msg=W0404
            from locale import getpreferredencoding
            encoding = getpreferredencoding()
            def decode_string_option(value):
                """Decode a string option."""
                return value.decode(encoding)

        for name in settings:
            if name not in cls._defs:
                logger.debug("get_arg_parser: ignoring unknown option {0}"
                                                                .format(name))
                return
            setting = cls._defs[name]
            if not setting.cmdline_help:
                logger.debug("get_arg_parser: option {0} has no cmdline"
                                                                .format(name))
                return
            if sys.version_info.major < 3:
                name = name.encode(encoding, "replace")
            option = option_prefix + name.replace("_", "-")
            dest = "pyxmpp2_" + name
            if setting.validator:
                opt_type = setting.validator
            elif setting.type is unicode and sys.version_info.major < 3:
                opt_type = decode_string_option
            else:
                opt_type = setting.type
            if setting.default_d:
                default_s = setting.default_d
                if sys.version_info.major < 3:
                    default_s = default_s.encode(encoding, "replace")
            elif setting.default is not None:
                default_s = repr(setting.default)
            else:
                default_s = None
            opt_help = setting.cmdline_help
            if sys.version_info.major < 3:
                opt_help = opt_help.encode(encoding, "replace")
            if default_s:
                opt_help += " (Default: {0})".format(default_s)
            if opt_type is bool:
                opt_action = _YesNoAction
            else:
                opt_action = "store"
            parser.add_argument(option,
                                action = opt_action,
                                default = setting.default,
                                type = opt_type,
                                help = opt_help,
                                metavar = name.upper(),
                                dest = dest)
        return parser
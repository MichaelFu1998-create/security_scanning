def load_arguments(self, args):
        """Load settings from :std:`ArgumentParser` output.

        :Parameters:
            - `args`: output of argument parsed based on the one
              returned by `get_arg_parser()`
        """
        for name, setting in self._defs.items():
            if sys.version_info.major < 3:
                # pylint: disable-msg=W0404
                from locale import getpreferredencoding
                encoding = getpreferredencoding()
                name = name.encode(encoding, "replace")
            attr = "pyxmpp2_" + name
            try:
                self[setting.name] = getattr(args, attr)
            except AttributeError:
                pass
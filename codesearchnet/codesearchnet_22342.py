def bind(mod_path, with_path=None):
        """
        bind user variable to `_wrapped`

        .. note::

            you don't need call this method by yourself.

            program will call it in  `cliez.parser.parse`


        .. expection::

            if path is not correct,will cause an `ImportError`


        :param str mod_path: module path, *use dot style,'mod.mod1'*
        :param str with_path: add path to `sys.path`,
            if path is file,use its parent.
        :return: A instance of `Settings`
        """

        if with_path:
            if os.path.isdir(with_path):
                sys.path.insert(0, with_path)
            else:
                sys.path.insert(0, with_path.rsplit('/', 2)[0])
            pass

        # raise `ImportError` mod_path if not exist
        mod = importlib.import_module(mod_path)

        settings = Settings()

        for v in dir(mod):
            if v[0] == '_' or type(getattr(mod, v)).__name__ == 'module':
                continue
            setattr(settings, v, getattr(mod, v))
            pass

        Settings._path = mod_path
        Settings._wrapped = settings

        return settings
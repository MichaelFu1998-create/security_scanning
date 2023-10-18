def parse_require(self, env, keys, defaults={}):
        """
        check and get require config
        :param dict env: user config node
        :param list keys: check keys
            .. note::

                option and key name must be same.

        :param dict defaults: default value for keys
        :return: dict.env with verified.


        .. exception::

            will raise `ValueError` when some key missed.

        """

        for k in keys:
            env[k] = getattr(self.options, k) or env.get(k, None)

            if env[k] is None:
                self.error("config syntax error,"
                           "please set `%s` in your env: %s" % (k, env))

            pass

        for k, v in defaults.items():
            env.setdefault(k, v)

        return env
def get(
        self,
        key: str,
        default: typing.Any = UNSET,
        type_: typing.Type[typing.Any] = str,
        subtype: typing.Type[typing.Any] = str,
        mapper: typing.Optional[typing.Callable[[object], object]] = None,
    ) -> typing.Any:
        """
        Parse a value from an environment variable.

        .. code-block:: python

           >>> os.environ['FOO']
           <<< '12345'
           >>>
           >>> os.environ['BAR']
           <<< '1,2,3,4'
           >>>
           >>> 'BAZ' in os.environ
           <<< False
           >>>
           >>> parser = Config()
           >>> parser.get('FOO', type_=int)
           <<< 12345
           >>>
           >>> parser.get('BAR', type_=list, subtype=int)
           <<< [1, 2, 3, 4]
           >>>
           >>> parser.get('BAZ', default='abc123')
           <<< 'abc123'
           >>>
           >>> parser.get('FOO', type_=int, mapper=lambda x: x*10)
           <<< 123450

        :param key: the key to look up the value under
        :param default: default value to return when when no value is present
        :param type\\_: the type to return
        :param subtype: subtype for iterator types
        :param mapper: a function to post-process the value with
        :return: the parsed config value

        """
        value = self.environ.get(key, UNSET)

        if value is UNSET and default is UNSET:
            raise ConfigError("Unknown environment variable: {0}".format(key))

        if value is UNSET:
            value = default
        else:
            value = self.parse(typing.cast(str, value), type_, subtype)

        if mapper:
            value = mapper(value)

        return value
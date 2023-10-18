def parse(
        self,
        value: str,
        type_: typing.Type[typing.Any] = str,
        subtype: typing.Type[typing.Any] = str,
    ) -> typing.Any:
        """
        Parse value from string.

        Convert :code:`value` to

        .. code-block:: python

           >>> parser = Config()
           >>> parser.parse('12345', type_=int)
           <<< 12345
           >>>
           >>> parser.parse('1,2,3,4', type_=list, subtype=int)
           <<< [1, 2, 3, 4]

        :param value: string
        :param type\\_: the type to return
        :param subtype: subtype for iterator types
        :return: the parsed config value

        """
        if type_ is bool:
            return type_(value.lower() in self.TRUE_STRINGS)

        try:
            if isinstance(type_, type) and issubclass(
                type_, (list, tuple, set, frozenset)
            ):
                return type_(
                    self.parse(v.strip(" "), subtype)
                    for v in value.split(",")
                    if value.strip(" ")
                )

            return type_(value)
        except ValueError as e:
            raise ConfigError(*e.args)
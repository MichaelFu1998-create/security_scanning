def native(cls, value):
        """
        Converts a CF* object into its python equivalent

        :param value:
            The CF* object to convert

        :return:
            The native python object
        """

        type_id = CoreFoundation.CFGetTypeID(value)
        if type_id in cls._native_map:
            return cls._native_map[type_id](value)
        else:
            return value
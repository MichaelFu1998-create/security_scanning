def addOptionBool(self, name, value):
        """
        .. _addOptionBool:

        Add a boolean option.

        :param name: The name of the option.
        :type name: str
        :param value: The value of the option.
        :type value: boolean
        :return: The result of the operation.
        :rtype: bool

        :see: addOption_, addOptionInt_, addOptionString_

        """
        return self.options.AddOptionBool(str_to_cppstr(name), value)
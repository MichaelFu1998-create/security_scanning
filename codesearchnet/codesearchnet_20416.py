def addOptionInt(self, name, value):
        """
        .. _addOptionInt:

        Add an integer option.

        :param name: The name of the option.
        :type name: str
        :param value: The value of the option.
        :type value: boolean
        :return: The result of the operation.
        :rtype: bool

        :see: addOption_, addOptionBool_, addOptionString_

        """
        return self.options.AddOptionInt(str_to_cppstr(name), value)
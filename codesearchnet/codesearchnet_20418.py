def addOption(self, name, value):
        """
        .. _addOption:

        Add an option.

        :param name: The name of the option.
        :type name: string
        :param value: The value of the option.
        :type value: boolean, integer, string
        :return: The result of the operation.
        :rtype: bool

        :see: addOptionBool_, addOptionInt_, addOptionString_

        """
        if name not in PyOptionList:
            return False
        if PyOptionList[name]['type'] == "String":
            return self.addOptionString(name, value)
        elif PyOptionList[name]['type'] == "Bool":
            return self.addOptionBool(name, value)
        elif PyOptionList[name]['type'] == "Int":
            return self.addOptionInt(name, value)
        return False
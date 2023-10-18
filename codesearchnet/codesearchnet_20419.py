def getOption(self, name):
        """
        .. _getOption:

        Retrieve option of a value.

        :param name: The name of the option.
        :type name: string
        :return: The value
        :rtype: boolean, integer, string or None

        :see: getOptionAsBool_, getOptionAsInt_, getOptionAsString_

        """
        if name not in PyOptionList:
            return None
        if PyOptionList[name]['type'] == "String":
            return self.getOptionAsString(name)
        elif PyOptionList[name]['type'] == "Bool":
            return self.getOptionAsBool(name)
        elif PyOptionList[name]['type'] == "Int":
            return self.getOptionAsInt(name)
        return False
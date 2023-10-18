def addOptionString(self, name, value, append=False):
        """
        .. _addOptionString:

        Add a string option.

        :param name: The name of the option.  Option names are case insensitive and must be unique.
        :type name: str
        :param value: The value of the option.
        :type value: str
        :param append: Setting append to true will cause values read from the command line
         or XML file to be concatenated into a comma delimited set.  If _append is false,
         newer values will overwrite older ones.
        :type append: boolean
        :return: The result of the operation.
        :rtype: bool

        :see: addOption_, addOptionBool_, addOptionInt_

        """
        return self.options.AddOptionString(
            str_to_cppstr(name), str_to_cppstr(value), append)
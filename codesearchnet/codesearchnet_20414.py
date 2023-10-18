def create(self, a, b, c):
        """
        .. _createoptions:

        Create an option object used to start the manager

        :param a: The path of the config directory
        :type a: str
        :param b: The path of the user directory
        :type b: str
        :param c: The "command line" options of the openzwave library
        :type c: str

        :see: destroyoptions_

        """
        self.options = CreateOptions(
            str_to_cppstr(a), str_to_cppstr(b), str_to_cppstr(c))
        return True
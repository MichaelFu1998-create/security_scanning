def validate_name(self, name):
        """
        Can the name be used as a python module or package?
        Raises ``ValueError`` if the name is invalid.

        :param name: the name to check
        """
        if not name:
            raise ValueError("Name cannot be empty")

        # Can the name be used as an identifier in python (module or package name)
        if not name.isidentifier():
            raise ValueError("{} is not a valid identifier".format(name))
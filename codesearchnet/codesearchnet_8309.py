def get(self, key, default=None):
        """ Return the key if exists or a default value

            :param str value: Value
            :param str default: Default value if key not present
        """
        if key in self:
            return self.__getitem__(key)
        else:
            return default
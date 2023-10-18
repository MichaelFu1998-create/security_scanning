def get(self, key, default=None):
        """
        :return: the value behind :paramref:`key` in the specification.
          If no value was found, :paramref:`default` is returned.
        :param key: a :ref:`specification key <prototype-key>`
        """
        for base in self.__specification:
            if key in base:
                return base[key]
        return default
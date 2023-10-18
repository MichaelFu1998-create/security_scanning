def __snake_case(self, descriptor):
        """
        Utility method to convert camelcase to snake
        :param descriptor: The dictionary to convert
        """
        newdict = {}
        for i, (k, v) in enumerate(descriptor.items()):
            newkey = ""
            for j, c in enumerate(k):
                if c.isupper():
                    if len(newkey) != 0:
                        newkey += '_'
                    newkey += c.lower()
                else:
                    newkey += c
            newdict[newkey] = v

        return newdict
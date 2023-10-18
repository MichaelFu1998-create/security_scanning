def match(self, uri):
        """ Check to see if this URI is retrievable by this Retriever implementation

        :param uri: the URI of the resource to be retrieved
        :type uri: str
        :return: True if it can be, False if not
        :rtype: bool
        """
        absolute_uri = self.__absolute__(uri)

        return absolute_uri.startswith(self.__path__) and op.exists(absolute_uri)
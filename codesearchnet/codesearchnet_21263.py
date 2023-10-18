def resolve(self, uri):
        """ Resolve a Resource identified by URI
        :param uri: The URI of the resource to be resolved
        :type uri: str
        :return: the contents of the resource as a string
        :rtype: str
        """
        for r in self.__retrievers__:
            if r.match(uri):
                return r
        raise UnresolvableURIError()
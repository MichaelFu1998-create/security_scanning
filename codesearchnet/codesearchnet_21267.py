def read(self, uri):
        """ Retrieve the contents of the resource

        :param uri: the URI of the resource to be retrieved
        :type uri: str
        :return: the contents of the resource
        :rtype: str
        """
        return self.__resolver__.getTextualNode(uri).export(Mimetypes.XML.TEI), "text/xml"
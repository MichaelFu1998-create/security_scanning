def read(self, uri):
        """ Retrieve the contents of the resource

        :param uri: the URI of the resource to be retrieved
        :type uri: str
        :return: the contents of the resource
        :rtype: str
        """
        uri = self.__absolute__(uri)
        mime, _ = guess_type(uri)
        if "image" in mime:
            return send_file(uri), mime
        else:
            with open(uri, "r") as f:
                file = f.read()
        return file, mime
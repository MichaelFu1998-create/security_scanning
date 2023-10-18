def r_annotation_body(self, sha):
        """ Route to retrieve contents of an annotation resource

        :param uri: The uri of the annotation resource
        :type uri: str
        :return: annotation contents
        :rtype: {str: Any}
        """
        annotation = self.__queryinterface__.getResource(sha)
        if not annotation:
            return "invalid resource uri", 404
        # TODO this should inspect the annotation content
        # set appropriate Content-Type headers
        # and return the actual content
        content = annotation.read()
        if isinstance(content, Response):
            return content
        headers = {"Content-Type": annotation.mimetype}
        return Response(content, headers=headers)
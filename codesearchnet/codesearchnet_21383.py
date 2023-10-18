def r_annotation(self, sha):
        """ Route to retrieve contents of an annotation resource

        :param uri: The uri of the annotation resource
        :type uri: str
        :return: annotation contents
        :rtype: {str: Any}
        """
        annotation = self.__queryinterface__.getResource(sha)
        if not annotation:
            return "invalid resource uri", 404
        response = {
            "@context": type(self).JSONLD_CONTEXT,
            "id": url_for(".r_annotation", sha=annotation.sha),
            "body": url_for(".r_annotation_body", sha=annotation.sha),
            "type": "Annotation",
            "target": annotation.target.to_json(),
            "owl:sameAs": [annotation.uri],
            "dc:type": annotation.type_uri,
            "nemo:slug": annotation.slug
        }
        return jsonify(response)
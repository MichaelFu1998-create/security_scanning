def r_annotations(self):
        """ Route to retrieve annotations by target

        :param target_urn: The CTS URN for which to retrieve annotations  
        :type target_urn: str
        :return: a JSON string containing count and list of resources
        :rtype: {str: Any}
        """

        target = request.args.get("target", None)
        wildcard = request.args.get("wildcard", ".", type=str)
        include = request.args.get("include")
        exclude = request.args.get("exclude")
        limit = request.args.get("limit", None, type=int)
        start = request.args.get("start", 1, type=int)
        expand = request.args.get("expand", False, type=bool)

        if target:

            try:
                urn = MyCapytain.common.reference.URN(target)
            except ValueError:
                return "invalid urn", 400

            count, annotations = self.__queryinterface__.getAnnotations(urn, wildcard=wildcard, include=include,
                                                                        exclude=exclude, limit=limit, start=start,
                                                                        expand=expand)
        else:
            #  Note that this implementation is not done for too much annotations
            #  because we do not implement pagination here
            count, annotations = self.__queryinterface__.getAnnotations(None, limit=limit, start=start, expand=expand)
        mapped = []
        response = {
            "@context": type(self).JSONLD_CONTEXT,
            "id": url_for(".r_annotations", start=start, limit=limit),
            "type": "AnnotationCollection",
            "startIndex": start,
            "items": [
            ],
            "total": count
        }
        for a in annotations:
            mapped.append({
                "id": url_for(".r_annotation", sha=a.sha),
                "body": url_for(".r_annotation_body", sha=a.sha),
                "type": "Annotation",
                "target": a.target.to_json(),
                "dc:type": a.type_uri,
                "owl:sameAs": [a.uri],
                "nemo:slug": a.slug
            })
        response["items"] = mapped
        response = jsonify(response)
        return response
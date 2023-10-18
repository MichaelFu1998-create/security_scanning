def get_reffs(self, objectId, subreference=None, collection=None, export_collection=False):
        """ Retrieve and transform a list of references.

        Returns the inventory collection object with its metadata and a callback function taking a level parameter \
        and returning a list of strings.

        :param objectId: Collection Identifier
        :type objectId: str
        :param subreference: Subreference from which to retrieve children
        :type subreference: str
        :param collection: Collection object bearing metadata
        :type collection: Collection
        :param export_collection: Return collection metadata
        :type export_collection: bool
        :return: Returns either the list of references, or the text collection object with its references as tuple
        :rtype: (Collection, [str]) or [str]
        """
        if collection is not None:
            text = collection
        else:
            text = self.get_collection(objectId)
        reffs = self.chunk(
            text,
            lambda level: self.resolver.getReffs(objectId, level=level, subreference=subreference)
        )
        if export_collection is True:
            return text, reffs
        return reffs
def process(self, nemo):
        """ Register nemo and parses annotations

        .. note:: Process parses the annotation and extends informations about the target URNs by retrieving resource in range

        :param nemo: Nemo
        """
        self.__nemo__ = nemo
        for annotation in self.__annotations__:
            annotation.target.expanded = frozenset(
                self.__getinnerreffs__(
                    objectId=annotation.target.objectId,
                    subreference=annotation.target.subreference
                )
            )
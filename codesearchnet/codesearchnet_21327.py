def get_passage(self, objectId, subreference):
        """ Retrieve the passage identified by the parameters

        :param objectId: Collection Identifier
        :type objectId: str
        :param subreference: Subreference of the passage
        :type subreference: str
        :return: An object bearing metadata and its text
        :rtype: InteractiveTextualNode
        """
        passage = self.resolver.getTextualNode(
            textId=objectId,
            subreference=subreference,
            metadata=True
        )
        return passage
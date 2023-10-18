def facts(self, **kwargs):
        """Get all facts of this node. Additional arguments may also be
        specified that will be passed to the query function.
        """
        return self.__api.facts(query=EqualsOperator("certname", self.name),
                                **kwargs)
def reports(self, **kwargs):
        """Get all reports for this node. Additional arguments may also be
        specified that will be passed to the query function.
        """
        return self.__api.reports(
            query=EqualsOperator("certname", self.name),
            **kwargs)
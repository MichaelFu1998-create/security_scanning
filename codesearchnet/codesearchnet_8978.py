def events(self, **kwargs):
        """Get all events for this report. Additional arguments may also be
        specified that will be passed to the query function.
        """
        return self.__api.events(query=EqualsOperator("report", self.hash_),
                                 **kwargs)
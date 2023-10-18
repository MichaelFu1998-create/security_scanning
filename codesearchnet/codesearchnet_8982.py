def resource(self, type_, title, **kwargs):
        """Get a resource matching the supplied type and title. Additional
        arguments may also be specified that will be passed to the query
        function.
        """
        resources = self.__api.resources(
            type_=type_,
            title=title,
            query=EqualsOperator("certname", self.name),
            **kwargs)
        return next(resource for resource in resources)
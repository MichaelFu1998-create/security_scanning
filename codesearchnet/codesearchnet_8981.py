def resources(self, type_=None, title=None, **kwargs):
        """Get all resources of this node or all resources of the specified
        type. Additional arguments may also be specified that will be passed
        to the query function.
        """
        if type_ is None:
            resources = self.__api.resources(
                query=EqualsOperator("certname", self.name),
                **kwargs)
        elif type_ is not None and title is None:
            resources = self.__api.resources(
                type_=type_,
                query=EqualsOperator("certname", self.name),
                **kwargs)
        else:
            resources = self.__api.resources(
                type_=type_,
                title=title,
                query=EqualsOperator("certname", self.name),
                **kwargs)
        return resources
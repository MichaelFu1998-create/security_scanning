def remove_resource(self, name):
        """https://github.com/frictionlessdata/datapackage-py#package
        """
        resource = self.get_resource(name)
        if resource:
            predicat = lambda resource: resource.get('name') != name
            self.__current_descriptor['resources'] = list(filter(
                predicat, self.__current_descriptor['resources']))
            self.__build()
        return resource
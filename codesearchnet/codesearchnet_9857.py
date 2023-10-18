def add_resource(self, descriptor):
        """https://github.com/frictionlessdata/datapackage-py#package
        """
        self.__current_descriptor.setdefault('resources', [])
        self.__current_descriptor['resources'].append(descriptor)
        self.__build()
        return self.__resources[-1]
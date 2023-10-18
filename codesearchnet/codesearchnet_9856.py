def get_resource(self, name):
        """https://github.com/frictionlessdata/datapackage-py#package
        """
        for resource in self.resources:
            if resource.name == name:
                return resource
        return None
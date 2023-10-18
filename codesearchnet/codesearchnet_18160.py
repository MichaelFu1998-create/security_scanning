def create(self, **kwargs):
        """
        Create a resource on the server
        :params kwargs: Attributes (field names and values) of the new resource
        """
        resource = self.resource_class(self.client)
        resource.update_from_dict(kwargs)
        resource.save(force_create=True)

        return resource
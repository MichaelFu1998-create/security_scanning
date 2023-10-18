def get_collection_endpoint(cls):
        """
        Get the relative path to the API resource collection

        If self.collection_endpoint is not set, it will default to the lowercase name of the resource class plus an "s" and the terminating "/"
        :param cls: Resource class
        :return: Relative path to the resource collection
        """
        return cls.Meta.collection_endpoint if cls.Meta.collection_endpoint is not None else cls.__name__.lower() + "s/"
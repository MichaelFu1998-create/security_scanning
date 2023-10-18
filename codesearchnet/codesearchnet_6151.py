def create_empty_resource(self, name):
        """Create an empty (length-0) resource.

        See DAVResource.create_empty_resource()
        """
        assert "/" not in name
        if self.provider.readonly:
            raise DAVError(HTTP_FORBIDDEN)
        path = util.join_uri(self.path, name)
        fp = self.provider._loc_to_file_path(path, self.environ)
        f = open(fp, "wb")
        f.close()
        return self.provider.get_resource_inst(path, self.environ)
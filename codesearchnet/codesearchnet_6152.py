def create_collection(self, name):
        """Create a new collection as member of self.

        See DAVResource.create_collection()
        """
        assert "/" not in name
        if self.provider.readonly:
            raise DAVError(HTTP_FORBIDDEN)
        path = util.join_uri(self.path, name)
        fp = self.provider._loc_to_file_path(path, self.environ)
        os.mkdir(fp)
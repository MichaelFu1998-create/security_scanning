def create_empty_resource(self, name):
        """Create and return an empty (length-0) resource as member of self.

        See DAVResource.create_empty_resource()
        """
        assert self.is_collection
        self._check_write_access()
        filepath = self._getFilePath(name)
        f = open(filepath, "w")
        f.close()
        commands.add(self.provider.ui, self.provider.repo, filepath)
        # get_resource_inst() won't work, because the cached manifest is outdated
        #        return self.provider.get_resource_inst(self.path.rstrip("/")+"/"+name, self.environ)
        return HgResource(
            self.path.rstrip("/") + "/" + name,
            False,
            self.environ,
            self.rev,
            self.localHgPath + "/" + name,
        )
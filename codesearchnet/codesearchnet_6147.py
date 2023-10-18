def move_recursive(self, dest_path):
        """See DAVResource.move_recursive() """
        if self.provider.readonly:
            raise DAVError(HTTP_FORBIDDEN)
        fpDest = self.provider._loc_to_file_path(dest_path, self.environ)
        assert not util.is_equal_or_child_uri(self.path, dest_path)
        assert not os.path.exists(fpDest)
        _logger.debug("move_recursive({}, {})".format(self._file_path, fpDest))
        shutil.move(self._file_path, fpDest)
        # (Live properties are copied by copy2 or copystat)
        # Move dead properties
        if self.provider.prop_manager:
            destRes = self.provider.get_resource_inst(dest_path, self.environ)
            self.provider.prop_manager.move_properties(
                self.get_ref_url(),
                destRes.get_ref_url(),
                with_children=True,
                environ=self.environ,
            )
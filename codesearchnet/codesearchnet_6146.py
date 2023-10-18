def copy_move_single(self, dest_path, is_move):
        """See DAVResource.copy_move_single() """
        if self.provider.readonly:
            raise DAVError(HTTP_FORBIDDEN)
        fpDest = self.provider._loc_to_file_path(dest_path, self.environ)
        assert not util.is_equal_or_child_uri(self.path, dest_path)
        # Copy file (overwrite, if exists)
        shutil.copy2(self._file_path, fpDest)
        # (Live properties are copied by copy2 or copystat)
        # Copy dead properties
        propMan = self.provider.prop_manager
        if propMan:
            destRes = self.provider.get_resource_inst(dest_path, self.environ)
            if is_move:
                propMan.move_properties(
                    self.get_ref_url(),
                    destRes.get_ref_url(),
                    with_children=False,
                    environ=self.environ,
                )
            else:
                propMan.copy_properties(
                    self.get_ref_url(), destRes.get_ref_url(), self.environ
                )
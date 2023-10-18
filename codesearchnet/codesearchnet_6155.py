def _loc_to_file_path(self, path, environ=None):
        """Convert resource path to a unicode absolute file path.
        Optional environ argument may be useful e.g. in relation to per-user
        sub-folder chrooting inside root_folder_path.
        """
        root_path = self.root_folder_path
        assert root_path is not None
        assert compat.is_native(root_path)
        assert compat.is_native(path)

        path_parts = path.strip("/").split("/")
        file_path = os.path.abspath(os.path.join(root_path, *path_parts))
        if not file_path.startswith(root_path):
            raise RuntimeError(
                "Security exception: tried to access file outside root: {}".format(
                    file_path
                )
            )

        # Convert to unicode
        file_path = util.to_unicode_safe(file_path)
        return file_path
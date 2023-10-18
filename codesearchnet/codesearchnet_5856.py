def delete(self, file_id):
        """
        Remove a specific file from the File Manager.

        :param file_id: The unique id for the File Manager file.
        :type file_id: :py:class:`str`
        """
        self.file_id = file_id
        return self._mc_client._delete(url=self._build_path(file_id))
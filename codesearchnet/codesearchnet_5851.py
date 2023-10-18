def delete(self, folder_id):
        """
        Delete a specific campaign folder, and mark all the campaigns in the
        folder as ‘unfiled’.

        :param folder_id: The unique id for the campaign folder.
        :type folder_id: :py:class:`str`
        """
        self.folder_id = folder_id
        return self._mc_client._delete(url=self._build_path(folder_id))
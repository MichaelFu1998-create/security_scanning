def _store_dicom_paths(self, folders):
        """Search for dicoms in folders and save file paths into
        self.dicom_paths set.

        :param folders: str or list of str
        """
        if isinstance(folders, str):
            folders = [folders]

        for folder in folders:

            if not os.path.exists(folder):
                raise FolderNotFound(folder)

            self.items.extend(list(find_all_dicom_files(folder)))
def add_cti_file(self, file_path: str):
        """
        Adds a CTI file to work with to the CTI file list.

        :param file_path: Set a file path to the target CTI file.

        :return: None.
        """
        if not os.path.exists(file_path):
            self._logger.warning(
                'Attempted to add {0} which does not exist.'.format(file_path)
            )

        if file_path not in self._cti_files:
            self._cti_files.append(file_path)
            self._logger.info(
                'Added {0} to the CTI file list.'.format(file_path)
            )
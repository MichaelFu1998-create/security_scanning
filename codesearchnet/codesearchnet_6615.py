def remove_cti_file(self, file_path: str):
        """
        Removes the specified CTI file from the CTI file list.

        :param file_path: Set a file path to the target CTI file.

        :return: None.
        """
        if file_path in self._cti_files:
            self._cti_files.remove(file_path)
            self._logger.info(
                'Removed {0} from the CTI file list.'.format(file_path)
            )
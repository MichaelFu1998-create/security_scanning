def list_files(self, dataset_id, glob=".", is_dir=False):
        """
        List matched filenames in a dataset on Citrination.

        :param dataset_id: The ID of the dataset to search for files.
        :type dataset_id: int
        :param glob: A pattern which will be matched against files in the dataset.
        :type glob: str
        :param is_dir: A boolean indicating whether or not the pattern should match against the beginning of paths in the dataset.
        :type is_dir: bool
        :return: A list of filepaths in the dataset matching the provided glob.
        :rtype: list of strings
        """
        data = {
            "list": {
                "glob": glob,
                "isDir": is_dir
            }
        }
        return self._get_success_json(self._post_json(routes.list_files(dataset_id), data, failure_message="Failed to list files for dataset {}".format(dataset_id)))['files']
def matched_file_count(self, dataset_id, glob=".", is_dir=False):
        """
        Returns the number of files matching a pattern in a dataset.

        :param dataset_id: The ID of the dataset to search for files.
        :type dataset_id: int
        :param glob: A pattern which will be matched against files in the dataset.
        :type glob: str
        :param is_dir: A boolean indicating whether or not the pattern should match against the beginning of paths in the dataset.
        :type is_dir: bool
        :return: The number of matching files
        :rtype: int
        """
        list_result = self.list_files(dataset_id, glob, is_dir)
        return len(list_result)
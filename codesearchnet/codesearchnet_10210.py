def get_dataset_file(self, dataset_id, file_path, version = None):
        """
        Retrieves a dataset file matching a provided file path

        :param dataset_id: The id of the dataset to retrieve file from
        :type dataset_id: int
        :param file_path: The file path within the dataset
        :type file_path: str
        :param version: The dataset version to look for the file in. If nothing is supplied, the latest dataset version will be searched
        :type version: int
        :return: A dataset file matching the filepath provided
        :rtype: :class:`DatasetFile`
        """
        return self.get_dataset_files(dataset_id, "^{}$".format(file_path), version_number=version)[0]
def get_dataset_files(self, dataset_id, glob=".", is_dir=False, version_number=None):
        """
        Retrieves URLs for the files matched by a glob or a path to a directory
        in a given dataset.

        :param dataset_id: The id of the dataset to retrieve files from
        :type dataset_id: int
        :param glob: A regex used to select one or more files in the dataset
        :type glob: str
        :param is_dir: Whether or not the supplied pattern should be treated as a directory to search in
        :type is_dir: bool
        :param version_number: The version number of the dataset to retrieve files from
        :type version_number: int
        :return: A list of dataset files whose paths match the provided pattern.
        :rtype: list of :class:`DatasetFile`
        """
        if version_number is None:
            latest = True
        else:
            latest = False

        data = {
            "download_request": {
                "glob": glob,
                "isDir": is_dir,
                "latest": latest
            }
        }

        failure_message = "Failed to get matched files in dataset {}".format(dataset_id)

        versions = self._get_success_json(self._post_json(routes.matched_files(dataset_id), data, failure_message=failure_message))['versions']

        # if you don't provide a version number, only the latest
        # will be included in the response body
        if version_number is None:
            version = versions[0]
        else:
            try:
                version = list(filter(lambda v: v['number'] == version_number, versions))[0]
            except IndexError:
                raise ResourceNotFoundException()

        return list(
            map(
                lambda f: DatasetFile(path=f['filename'], url=f['url']), version['files']
                )
            )
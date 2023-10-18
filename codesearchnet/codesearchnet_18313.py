def _load_all_in_directory(self) -> Dict[str, Iterable[DataSourceType]]:
        """
        Loads all of the data from the files in directory location.
        :return: a origin map of all the loaded data
        """
        origin_mapped_data = dict()    # type: Dict[str, Iterable[DataSourceType]]
        for file_path in glob.iglob("%s/**/*" % self._directory_location, recursive=True):
            if self.is_data_file(file_path):
                origin_mapped_data[file_path] = self.no_error_extract_data_from_file(file_path)
        return origin_mapped_data
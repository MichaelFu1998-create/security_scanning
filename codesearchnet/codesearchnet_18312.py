def no_error_extract_data_from_file(self, file_path: str) -> Iterable[DataSourceType]:
        """
        Proxy for `extract_data_from_file` that suppresses any errors and instead just returning an empty list.
        :param file_path: see `extract_data_from_file`
        :return: see `extract_data_from_file`
        """
        try:
            return self.extract_data_from_file(file_path)
        except Exception as e:
            logging.warning(e)
            return []
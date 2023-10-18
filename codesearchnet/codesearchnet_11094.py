def get_data(self, label: str) -> Any:
        """
        Get a data resource by label

        Args:
            label (str): The labvel for the data resource to fetch

        Returns:
            The requeted data object
        """
        return self._get_resource(label, self._data, "data")
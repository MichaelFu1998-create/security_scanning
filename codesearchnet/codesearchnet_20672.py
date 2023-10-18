def search_unique(self, table_name, sample, unique_fields=None):
        """ Search in `table` an item with the value of the `unique_fields` in the `data` sample.
        Check if the the obtained result is unique. If nothing is found will return an empty list,
        if there is more than one item found, will raise an IndexError.

        Parameters
        ----------
        table_name: str

        sample: dict
            Sample data

        unique_fields: list of str
            Name of fields (keys) from `data` which are going to be used to build
            a sample to look for exactly the same values in the database.
            If None, will use every key in `data`.

        Returns
        -------
        eid: int
            Id of the object found with same `unique_fields`.
            None if none is found.

        Raises
        ------
        MoreThanOneItemError
            If more than one example is found.
        """
        return search_unique(table=self.table(table_name),
                             sample=sample,
                             unique_fields=unique_fields)
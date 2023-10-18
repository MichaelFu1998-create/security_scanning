def search_sample(self, table_name, sample):
        """Search for items in `table` that have the same field sub-set values as in `sample`.

        Parameters
        ----------
        table_name: str

        sample: dict
            Sample data

        Returns
        -------
        search_result: list of dict
            List of the items found. The list is empty if no item is found.
        """
        return search_sample(table=self.table(table_name),
                             sample=sample)
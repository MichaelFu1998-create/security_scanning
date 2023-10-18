def count(self, table_name, sample):
        """Return the number of items that match the `sample` field values
        in table `table_name`.
        Check function search_sample for more details.
        """
        return len(list(search_sample(table=self.table(table_name),
                                      sample=sample)))
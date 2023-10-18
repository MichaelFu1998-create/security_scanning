def is_unique(self, table_name, sample, unique_fields=None):
        """Return True if an item with the value of `unique_fields`
        from `data` is unique in the table with `table_name`.
        False if no sample is found or more than one is found.

        See function `find_unique` for more details.

        Parameters
        ----------
        table_name: str

        sample: dict
            Sample data for query

        unique_fields: str or list of str

        Returns
        -------
        is_unique: bool
        """
        try:
            eid = find_unique(self.table(table_name),
                              sample=sample,
                              unique_fields=unique_fields)
        except:
            return False
        else:
            return eid is not None
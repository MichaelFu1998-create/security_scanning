def search_by_eid(self, table_name, eid):
        """Return the element in `table_name` with Object ID `eid`.
        If None is found will raise a KeyError exception.

        Parameters
        ----------
        table_name: str
            The name of the table to look in.

        eid: int
            The Object ID of the element to look for.

        Returns
        -------
        elem: tinydb.database.Element

        Raises
        ------
        KeyError
            If the element with ID `eid` is not found.
        """
        elem = self.table(table_name).get(eid=eid)
        if elem is None:
            raise KeyError('Could not find {} with eid {}.'.format(table_name, eid))

        return elem
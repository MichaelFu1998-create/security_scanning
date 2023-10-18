def update_unique(self, table_name, fields, data, cond=None, unique_fields=None,
                      *, raise_if_not_found=False):
        """Update the unique matching element to have a given set of fields.

        Parameters
        ----------
        table_name: str

        fields: dict or function[dict -> None]
            new data/values to insert into the unique element
            or a method that will update the elements.

        data: dict
            Sample data for query

        cond: tinydb.Query
            which elements to update

        unique_fields: list of str

        raise_if_not_found: bool
            Will raise an exception if the element is not found for update.

        Returns
        -------
        eid: int
            The eid of the updated element if found, None otherwise.
        """
        eid = find_unique(self.table(table_name), data, unique_fields)

        if eid is None:
            if raise_if_not_found:
                msg  = 'Could not find {} with {}'.format(table_name, data)
                if cond is not None:
                    msg += ' where {}.'.format(cond)
                raise IndexError(msg)

        else:
            self.table(table_name).update(_to_string(fields), cond=cond, eids=[eid])

        return eid
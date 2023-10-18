def sort_by(self, field, asc=True):
        """
        Add a sortby field to the query

        - **field** - the name of the field to sort by
        - **asc** - when `True`, sorting will be done in asceding order
        """
        self._sortby = SortbyField(field, asc)
        return self
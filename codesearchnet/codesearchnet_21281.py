def get(self, pk):
        """ 
        Retreive a single record from the table.  Lots of reasons this might be
        best implemented in the model

        :pk:            The primary key ID for the record
        :returns:       List of single result
        """

        if type(pk) == str:
            # Probably an int, give it a shot
            try:
                pk = int(pk)
            except ValueError: pass

        return self.select(
            "SELECT {0} FROM " + self.table + " WHERE " + self.pk + " = {1};",
            self.columns, pk)
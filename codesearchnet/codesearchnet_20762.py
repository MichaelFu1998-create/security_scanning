def row(self, idx):
        """
        Returns DataFrameRow of the DataFrame given its index.

        :param idx: the index of the row in the DataFrame.
        :return: returns a DataFrameRow
        """
        return DataFrameRow(idx, [x[idx] for x in self], self.colnames)
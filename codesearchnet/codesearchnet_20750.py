def subset(self, *args):
        """
        Subset only some of the columns of the DataFrame.

        :param args: list of column names of the object that should be subsetted
        :type args: tuple
        :return: returns dataframe with only the columns you selected
        :rtype: DataFrame
        """
        cols = {}
        for k in self.colnames:
            if k in args:
                cols[str(k)] = \
                    self.__data_columns[self.colnames.index(k)].values
        return DataFrame(**cols)
def subset(self, *args):
        """
        Subset only some of the columns of the DataFrame.

        :param args: list of column names of the object that should be subsetted
        :type args: tuple
        :return: returns DataFrame with only the columns you selected
        :rtype: DataFrame
        """
        args = list(args)
        args.extend([x for x in
                     self.__grouping.grouping_colnames if x not in args])
        return GroupedDataFrame(self.__grouping.ungroup().subset(*args),
                                *self.__grouping.grouping_colnames)
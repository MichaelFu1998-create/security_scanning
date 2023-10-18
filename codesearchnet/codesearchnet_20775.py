def modify(self, clazz, new_col, *args):
        """
        Modify some columns (i.e. apply a function)
         and add the result to the table.

        :param clazz: name of a class that extends class Callable
        :type clazz: class
        :param new_col: name of the new column
        :type new_col: str
        :param args: list of column names of the object that
         function should be applied to
        :type args: tuple
        :return: returns a new GroupedDataFrame object with the modified
          values, i.e. the new column of values
        :rtype: GroupedDataFrame
        """
        if is_callable(clazz) \
                and not is_none(new_col) \
                and has_elements(*args) \
                and is_disjoint(self.__grouping.grouping_colnames,
                                args,
                                __DISJOINT_SETS_ERROR__):
            return self.__do_modify(clazz, new_col, *args)
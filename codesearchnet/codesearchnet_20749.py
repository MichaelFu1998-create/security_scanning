def aggregate(self, clazz, new_col, *args):
        """
        Aggregate the rows of the DataFrame into a single value.

        :param clazz: name of a class that extends class Callable
        :type clazz: class
        :param new_col: name of the new column
        :type new_col: str
        :param args: list of column names of the object that function 
        should be applied to
        :type args: tuple
        :return: returns a new dataframe object with the aggregated value
        :rtype: DataFrame
        """
        if is_callable(clazz) and not is_none(new_col) and has_elements(*args):
            return self.__do_aggregate(clazz, new_col, *args)
def process_columns(self, columns):
        """ 
        Handle provided columns and if necessary, convert columns to a list for 
        internal strage.

        :columns: A sequence of columns for the table. Can be list, comma
            -delimited string, or IntEnum.
        """
        if type(columns) == list:
            self.columns = columns
        elif type(columns) == str:
            self.columns = [c.strip() for c in columns.split()]
        elif type(columns) == IntEnum:
            self.columns = [str(c) for c in columns]
        else:
            raise RawlException("Unknown format for columns")
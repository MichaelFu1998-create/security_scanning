def _assemble_select(self, sql_str, columns, *args, **kwargs):
        """ Alias for _assemble_with_columns
        """
        warnings.warn("_assemble_select has been depreciated for _assemble_with_columns. It will be removed in a future version.", DeprecationWarning)
        return self._assemble_with_columns(sql_str, columns, *args, **kwargs)
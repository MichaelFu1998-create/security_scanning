def load(self, val, **kwargs):
        """
        Load the file contents into the supplied pandas dataframe or
        HoloViews Table. This allows a selection to be made over the
        metadata before loading the file contents (may be slow).
        """
        if Table and isinstance(val, Table):
            return self.load_table(val, **kwargs)
        elif DataFrame and isinstance(val, DataFrame):
            return self.load_dframe(val, **kwargs)
        else:
            raise Exception("Type %s not a DataFrame or Table." % type(val))
def load_dframe(self, dframe):
        """
        Load the file contents into the supplied dataframe using the
        specified key and filetype.
        """
        filename_series = dframe[self.key]
        loaded_data = filename_series.map(self.filetype.data)
        keys = [list(el.keys()) for el in loaded_data.values]
        for key in set().union(*keys):
            key_exists = key in dframe.columns
            if key_exists:
                self.warning("Appending '_data' suffix to data key %r to avoid"
                             "overwriting existing metadata with the same name." % key)
            suffix = '_data' if key_exists else ''
            dframe[key+suffix] = loaded_data.map(lambda x: x.get(key, np.nan))
        return dframe
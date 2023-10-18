def _push_dfblock(self, key, df, ds_name, range_values):
        """
        :param key: string
        :param df: pandas Dataframe
        :param ds_name: string
        """
        #create numpy array and put into hdf_file
        vals_colranges = [range_values[x] for x in df.index.names]
        nu_shape = [len(x) for x in vals_colranges]

        return self.put(key, np.reshape(df.values, tuple(nu_shape)),
                        attrs={'axes': df.index.names},
                        ds_name=ds_name, append=True)
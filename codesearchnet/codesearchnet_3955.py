def to_csv(self, fname_radical, **kwargs):
        """
        Save data to the csv format by default, in two separate files.

        Optional keyword arguments can be passed to pandas.
        """
        if self.data is not None:
            self.data.to_csv(fname_radical+'_data.csv', index=False, **kwargs)
            pd.DataFrame(self.adjacency_matrix).to_csv(fname_radical \
                                                       + '_target.csv',
                                                       index=False, **kwargs)

        else:
            raise ValueError("Graph has not yet been generated. \
                              Use self.generate() to do so.")
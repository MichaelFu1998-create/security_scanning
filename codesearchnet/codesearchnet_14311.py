def transform(x):
        """
        Transform from date to a numerical format
        """
        try:
            x = date2num(x)
        except AttributeError:
            # numpy datetime64
            # This is not ideal because the operations do not
            # preserve the np.datetime64 type. May be need
            # a datetime64_trans
            x = [pd.Timestamp(item) for item in x]
            x = date2num(x)
        return x
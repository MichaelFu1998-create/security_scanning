def transform(x):
        """
        Transform from Timeddelta to numerical format
        """
        # microseconds
        try:
            x = np.array([_x.total_seconds()*10**6 for _x in x])
        except TypeError:
            x = x.total_seconds()*10**6
        return x
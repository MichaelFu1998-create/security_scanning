def transform(x):
        """
        Transform from Timeddelta to numerical format
        """
        # nanoseconds
        try:
            x = np.array([_x.value for _x in x])
        except TypeError:
            x = x.value
        return x
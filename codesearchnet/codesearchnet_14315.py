def inverse(x):
        """
        Transform to Timedelta from numerical format
        """
        try:
            x = [pd.Timedelta(int(i)) for i in x]
        except TypeError:
            x = pd.Timedelta(int(x))
        return x
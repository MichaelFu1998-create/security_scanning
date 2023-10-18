def inverse(x):
        """
        Transform to Timedelta from numerical format
        """
        try:
            x = [datetime.timedelta(microseconds=i) for i in x]
        except TypeError:
            x = datetime.timedelta(microseconds=x)
        return x
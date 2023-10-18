def _tidyup_labels(self, labels):
        """
        Make all labels uniform in format and remove redundant zeros
        for labels in exponential format.

        Parameters
        ----------
        labels : list-like
            Labels to be tidied.

        Returns
        -------
        out : list-like
            Labels
        """
        def remove_zeroes(s):
            """
            Remove unnecessary zeros for float string s
            """
            tup = s.split('e')
            if len(tup) == 2:
                mantissa = tup[0].rstrip('0').rstrip('.')
                exponent = int(tup[1])
                if exponent:
                    s = '%se%d' % (mantissa, exponent)
                else:
                    s = mantissa
            return s

        def as_exp(s):
            """
            Float string s as in exponential format
            """
            return s if 'e' in s else '{:1.0e}'.format(float(s))

        # If any are in exponential format, make all of
        # them expontential
        has_e = np.array(['e' in x for x in labels])
        if not np.all(has_e) and not np.all(~has_e):
            labels = [as_exp(x) for x in labels]

        labels = [remove_zeroes(x) for x in labels]
        return labels
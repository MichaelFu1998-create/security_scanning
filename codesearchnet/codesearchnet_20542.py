def set_labels(self, labels):
        """
        Parameters
        ----------
        labels: list of int or str
            This list will be checked to have the same size as

        Raises
        ------
        ValueError
            if len(labels) != self.n_subjs
        """
        if not isinstance(labels, string_types) and len(labels) != self.n_subjs:
            raise ValueError('The number of given labels ({}) is not the same '
                             'as the number of subjects ({}).'.format(len(labels), self.n_subjs))

        self.labels = labels
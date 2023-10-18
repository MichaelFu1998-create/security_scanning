def set_labels(self, subj_labels):
        """
        Parameters
        ----------
        subj_labels: list of int or str
            This list will be checked to have the same size as files list
            (self.items)
        """
        if len(subj_labels) != self.n_subjs:
            raise ValueError('The number of given labels is not the same as the number of subjects.')

        self.labels = subj_labels
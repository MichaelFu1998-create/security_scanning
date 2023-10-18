def well_rows(self, well_row, well_column):
        """All well rows in experiment. Equivalent to --U in files.

        Returns
        -------
        list of ints
        """
        return list(set([attribute(img, 'u') for img in self.images]))
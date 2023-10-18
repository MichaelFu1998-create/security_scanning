def field_columns(self, well_row, well_column):
        """Field columns for given well. Equivalent to --X in files.

        Parameters
        ----------
        well_row : int
            Starts at 0. Same as --V in files.
        well_column : int
            Starts at 0. Same as --U in files.

        Returns
        -------
        list of ints
            Columns found for specified well.
        """
        imgs = self.well_images(well_row, well_column)
        return list(set([attribute(img, 'x') for img in imgs]))
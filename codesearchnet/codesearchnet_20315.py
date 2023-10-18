def image(self, well_row, well_column, field_row, field_column):
        """Get path of specified image.

        Parameters
        ----------
        well_row : int
            Starts at 0. Same as --U in files.
        well_column : int
            Starts at 0. Same as --V in files.
        field_row : int
            Starts at 0. Same as --Y in files.
        field_column : int
            Starts at 0. Same as --X in files.

        Returns
        -------
        string
            Path to image or empty string if image is not found.
        """
        return next((i for i in self.images
                     if attribute(i, 'u') == well_column and
                        attribute(i, 'v') == well_row and
                        attribute(i, 'x') == field_column and
                        attribute(i, 'y') == field_row), '')
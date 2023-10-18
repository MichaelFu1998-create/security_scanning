def well_images(self, well_row, well_column):
        """Get list of paths to images in specified well.


        Parameters
        ----------
        well_row : int
            Starts at 0. Same as --V in files.
        well_column : int
            Starts at 0. Save as --U in files.

        Returns
        -------
        list of strings
            Paths to images or empty list if no images are found.
        """
        return list(i for i in self.images
                    if attribute(i, 'u') == well_column and
                       attribute(i, 'v') == well_row)
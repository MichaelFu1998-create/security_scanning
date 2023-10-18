def zoomed_scaled_array_around_mask(self, mask, buffer=1):
        """Extract the 2D region of an array corresponding to the rectangle encompassing all unmasked values.

        This is used to extract and visualize only the region of an image that is used in an analysis.

        Parameters
        ----------
        mask : mask.Mask
            The mask around which the scaled array is extracted.
        buffer : int
            The buffer of pixels around the extraction.
        """
        return self.new_with_array(array=array_util.extracted_array_2d_from_array_2d_and_coordinates(
            array_2d=self,  y0=mask.zoom_region[0]-buffer, y1=mask.zoom_region[1]+buffer,
            x0=mask.zoom_region[2]-buffer, x1=mask.zoom_region[3]+buffer))
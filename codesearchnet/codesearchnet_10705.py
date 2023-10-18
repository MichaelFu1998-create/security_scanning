def resized_scaled_array_from_array(self, new_shape, new_centre_pixels=None, new_centre_arcsec=None):
        """resized the array to a new shape and at a new origin.

        Parameters
        -----------
        new_shape : (int, int)
            The new two-dimensional shape of the array.
        """
        if new_centre_pixels is None and new_centre_arcsec is None:
            new_centre = (-1, -1)  # In Numba, the input origin must be the same image type as the origin, thus we cannot
            # pass 'None' and instead use the tuple (-1, -1).
        elif new_centre_pixels is not None and new_centre_arcsec is None:
            new_centre = new_centre_pixels
        elif new_centre_pixels is None and new_centre_arcsec is not None:
            new_centre = self.arc_second_coordinates_to_pixel_coordinates(arc_second_coordinates=new_centre_arcsec)
        else:
            raise exc.DataException('You have supplied two centres (pixels and arc-seconds) to the resize scaled'
                                       'array function')

        return self.new_with_array(array=array_util.resized_array_2d_from_array_2d_and_resized_shape(
            array_2d=self, resized_shape=new_shape, origin=new_centre))
def reconstructed_pixelization_from_solution_vector(self, solution_vector):
        """Given the solution vector of an inversion (see *inversions.Inversion*), determine the reconstructed \
        pixelization of the rectangular pixelization by using the mapper."""
        recon = mapping_util.map_unmasked_1d_array_to_2d_array_from_array_1d_and_shape(array_1d=solution_vector,
                                                                                       shape=self.shape)
        return scaled_array.ScaledRectangularPixelArray(array=recon, pixel_scales=self.geometry.pixel_scales,
                                                        origin=self.geometry.origin)
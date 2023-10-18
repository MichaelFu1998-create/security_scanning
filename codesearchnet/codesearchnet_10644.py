def frame_at_coordinates_jit(coordinates, mask, mask_index_array, psf):
        """ Compute the frame (indexes of pixels light is blurred into) and psf_frame (psf kernel values of those \
        pixels) for a given coordinate in a masks and its PSF.

        Parameters
        ----------
        coordinates: (int, int)
            The coordinates of mask_index_array on which the frame should be centred
        psf_shape: (int, int)
            The shape of the psf for which this frame will be used
        """

        psf_shape = psf.shape
        psf_max_size = psf_shape[0] * psf_shape[1]

        half_x = int(psf_shape[0] / 2)
        half_y = int(psf_shape[1] / 2)

        frame = -1 * np.ones((psf_max_size))
        psf_frame = -1.0 * np.ones((psf_max_size))

        count = 0
        for i in range(psf_shape[0]):
            for j in range(psf_shape[1]):
                x = coordinates[0] - half_x + i
                y = coordinates[1] - half_y + j
                if 0 <= x < mask_index_array.shape[0] and 0 <= y < mask_index_array.shape[1]:
                    value = mask_index_array[x, y]
                    if value >= 0 and not mask[x, y]:
                        frame[count] = value
                        psf_frame[count] = psf[i, j]
                        count += 1

        return frame, psf_frame
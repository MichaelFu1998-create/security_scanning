def pix_to_regular(self):
        """Compute the mappings between a pixelization's pixels and the unmasked regular-grid pixels. These mappings \
        are determined after the regular-grid is used to determine the pixelization.

        The pixelization's pixels map to different number of regular-grid pixels, thus a list of lists is used to \
        represent these mappings"""
        pix_to_regular = [[] for _ in range(self.pixels)]

        for regular_pixel, pix_pixel in enumerate(self.regular_to_pix):

            pix_to_regular[pix_pixel].append(regular_pixel)

        return pix_to_regular
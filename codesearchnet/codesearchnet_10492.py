def pix_to_sub(self):
        """Compute the mappings between a pixelization's pixels and the unmasked sub-grid pixels. These mappings \
        are determined after the regular-grid is used to determine the pixelization.

        The pixelization's pixels map to different number of sub-grid pixels, thus a list of lists is used to \
        represent these mappings"""
        pix_to_sub = [[] for _ in range(self.pixels)]

        for regular_pixel, pix_pixel in enumerate(self.sub_to_pix):
            pix_to_sub[pix_pixel].append(regular_pixel)

        return pix_to_sub
def mapping_matrix(self):
        """The mapping matrix is a matrix representing the mapping between every unmasked pixel of a grid and \
        the pixels of a pixelization. Non-zero entries signify a mapping, whereas zeros signify no mapping.

        For example, if the regular grid has 5 pixels and the pixelization 3 pixels, with the following mappings:

        regular pixel 0 -> pixelization pixel 0
        regular pixel 1 -> pixelization pixel 0
        regular pixel 2 -> pixelization pixel 1
        regular pixel 3 -> pixelization pixel 1
        regular pixel 4 -> pixelization pixel 2

        The mapping matrix (which is of dimensions regular_pixels x pixelization_pixels) would appear as follows:

        [1, 0, 0] [0->0]
        [1, 0, 0] [1->0]
        [0, 1, 0] [2->1]
        [0, 1, 0] [3->1]
        [0, 0, 1] [4->2]

        The mapping matrix is in fact built using the sub-grid of the grid-stack, whereby each regular-pixel is \
        divided into a regular grid of sub-pixels which are all paired to pixels in the pixelization. The entires \
        in the mapping matrix now become fractional values dependent on the sub-grid size. For example, for a 2x2 \
        sub-grid in each pixel (which means the fraction value is 1.0/(2.0^2) = 0.25, if we have the following mappings:

        regular pixel 0 -> sub pixel 0 -> pixelization pixel 0
        regular pixel 0 -> sub pixel 1 -> pixelization pixel 1
        regular pixel 0 -> sub pixel 2 -> pixelization pixel 1
        regular pixel 0 -> sub pixel 3 -> pixelization pixel 1
        regular pixel 1 -> sub pixel 0 -> pixelization pixel 1
        regular pixel 1 -> sub pixel 1 -> pixelization pixel 1
        regular pixel 1 -> sub pixel 2 -> pixelization pixel 1
        regular pixel 1 -> sub pixel 3 -> pixelization pixel 1
        regular pixel 2 -> sub pixel 0 -> pixelization pixel 2
        regular pixel 2 -> sub pixel 1 -> pixelization pixel 2
        regular pixel 2 -> sub pixel 2 -> pixelization pixel 3
        regular pixel 2 -> sub pixel 3 -> pixelization pixel 3

        The mapping matrix (which is still of dimensions regular_pixels x source_pixels) would appear as follows:

        [0.25, 0.75, 0.0, 0.0] [1 sub-pixel maps to pixel 0, 3 map to pixel 1]
        [ 0.0,  1.0, 0.0, 0.0] [All sub-pixels map to pixel 1]
        [ 0.0,  0.0, 0.5, 0.5] [2 sub-pixels map to pixel 2, 2 map to pixel 3]
        """
        return mapper_util.mapping_matrix_from_sub_to_pix(sub_to_pix=self.sub_to_pix, pixels=self.pixels,
                                                          regular_pixels=self.grid_stack.regular.shape[0],
                                                          sub_to_regular=self.grid_stack.sub.sub_to_regular,
                                                          sub_grid_fraction=self.grid_stack.sub.sub_grid_fraction)
def unmasked_sparse_to_sparse(self):
        """The 1D index mappings between the unmasked sparse-grid and masked sparse grid."""

        return mapping_util.unmasked_sparse_to_sparse_from_mask_and_pixel_centres(
            mask=self.regular_grid.mask,
            unmasked_sparse_grid_pixel_centres=self.unmasked_sparse_grid_pixel_centres,
            total_sparse_pixels=self.total_sparse_pixels).astype(
            'int')
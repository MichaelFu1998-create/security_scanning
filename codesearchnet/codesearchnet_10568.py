def sparse_to_unmasked_sparse(self):
        """The 1D index mappings between the masked sparse-grid and unmasked sparse grid."""
        return mapping_util.sparse_to_unmasked_sparse_from_mask_and_pixel_centres(
            total_sparse_pixels=self.total_sparse_pixels, mask=self.regular_grid.mask,
            unmasked_sparse_grid_pixel_centres=self.unmasked_sparse_grid_pixel_centres).astype('int')
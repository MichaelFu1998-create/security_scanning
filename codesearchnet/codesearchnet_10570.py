def sparse_grid(self):
        """The (y,x) arc-second coordinates of the masked sparse-grid."""
        return mapping_util.sparse_grid_from_unmasked_sparse_grid(
            unmasked_sparse_grid=self.unmasked_sparse_grid,
            sparse_to_unmasked_sparse=self.sparse_to_unmasked_sparse)
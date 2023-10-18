def regular_to_sparse(self):
        """The 1D index mappings between the regular-grid and masked sparse-grid."""

        return mapping_util.regular_to_sparse_from_sparse_mappings(
            regular_to_unmasked_sparse=self.regular_to_unmasked_sparse,
            unmasked_sparse_to_sparse=self.unmasked_sparse_to_sparse).astype('int')
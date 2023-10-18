def _calc_hash_da(self, rs):
        """Compute hash of D and A timestamps for single-step D+A case.
        """
        self.hash_d = hash_(rs.get_state())[:6]
        self.hash_a = self.hash_d
def get_chunk_meta_item(self, chunk_meta, grp, pug, chk):
        """Get item of chunk meta table"""
        num_chk = self.envs["NUM_CHK"]
        num_pu = self.envs["NUM_PU"]
        index = grp * num_pu * num_chk + pug * num_chk + chk
        return chunk_meta[index]
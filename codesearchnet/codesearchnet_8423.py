def get_chunk_meta(self, meta_file):
        """Get chunk meta table"""
        chunks = self.envs["CHUNKS"]
        if cij.nvme.get_meta(0, chunks * self.envs["CHUNK_META_SIZEOF"], meta_file):
            raise RuntimeError("cij.liblight.get_chunk_meta: fail")

        chunk_meta = cij.bin.Buffer(types=self.envs["CHUNK_META_STRUCT"], length=chunks)
        chunk_meta.read(meta_file)
        return chunk_meta
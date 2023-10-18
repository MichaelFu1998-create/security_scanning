def is_bad_chunk(self, chunk_meta, grp, pug, chk):
        """Check the chunk is offline or not"""
        meta = self.get_chunk_meta_item(chunk_meta, grp, pug, chk)
        if meta.CS & 0x8 != 0:
            return True
        return False
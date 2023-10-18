def is_open_chunk(self, chk):
        """Check the chunk is free or not"""
        cs = self.get_chunk_status(chk)
        if cs & 0x4 != 0:
            return True
        return False
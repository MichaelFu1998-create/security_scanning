def is_closed_chunk(self, chk):
        """Check the chunk is free or not"""
        cs = self.get_chunk_status(chk)
        if cs & 0x2 != 0:
            return True
        return False
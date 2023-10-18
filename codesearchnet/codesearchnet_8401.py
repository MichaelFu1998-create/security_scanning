def is_bad_chunk(self, chk, yml):
        """Check the chunk is offline or not"""
        cs = self.get_chunk_status(chk, yml)
        if cs >= 8:
            return True
        return False
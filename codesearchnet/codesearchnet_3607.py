def RETURN(self, offset, size):
        """Halt execution returning output data"""
        data = self.read_buffer(offset, size)
        raise EndTx('RETURN', data)
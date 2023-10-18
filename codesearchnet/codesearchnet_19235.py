def _compress(self, input_str):
        """
        Compress the log message in order to send less bytes to the wire.
        """
        compressed_bits = cStringIO.StringIO()
        
        f = gzip.GzipFile(fileobj=compressed_bits, mode='wb')
        f.write(input_str)
        f.close()
        
        return compressed_bits.getvalue()
def _zlib_compress(data, algorithm):
        '''GZIP compress'''

        if algorithm['subtype'] == 'deflate':
            encoder = zlib.compressobj(algorithm['level'], zlib.DEFLATED, -15)
            compressed = encoder.compress(data)
            compressed += encoder.flush()

            return compressed
        else:
            raise Exception('Compression subtype not supported: %s'
                            % algorithm['subtype'])
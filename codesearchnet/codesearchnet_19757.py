def _compress_data(self, data, options):
        '''Compress data'''

        compression_algorithm_id = options['compression_algorithm_id']
        if compression_algorithm_id not in self.compression_algorithms:
            raise Exception('Unknown compression algorithm id: %d'
                            % compression_algorithm_id)

        compression_algorithm = \
            self.compression_algorithms[compression_algorithm_id]

        algorithm = self._get_algorithm_info(compression_algorithm)

        compressed = self._encode(data, algorithm)

        if len(compressed) < len(data):
            data = compressed
        else:
            options['compression_algorithm_id'] = 0

        return data
def _decompress_data(self, data, options):
        '''Decompress data'''

        compression_algorithm_id = options['compression_algorithm_id']
        if compression_algorithm_id not in self.compression_algorithms:
            raise Exception('Unknown compression algorithm id: %d'
                            % compression_algorithm_id)

        compression_algorithm = \
            self.compression_algorithms[compression_algorithm_id]

        algorithm = self._get_algorithm_info(compression_algorithm)

        data = self._decode(data, algorithm)

        return data
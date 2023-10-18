def _unserialize_data(self, data, options):
        '''Unserialize data'''

        serialization_algorithm_id = options['serialization_algorithm_id']
        if serialization_algorithm_id not in self.serialization_algorithms:
            raise Exception('Unknown serialization algorithm id: %d'
                            % serialization_algorithm_id)

        serialization_algorithm = \
            self.serialization_algorithms[serialization_algorithm_id]

        algorithm = self._get_algorithm_info(serialization_algorithm)

        data = self._decode(data, algorithm)

        return data
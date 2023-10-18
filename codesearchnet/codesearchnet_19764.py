def _get_algorithm_info(self, algorithm_info):
        '''Get algorithm info'''

        if algorithm_info['algorithm'] not in self.ALGORITHMS:
            raise Exception('Algorithm not supported: %s'
                            % algorithm_info['algorithm'])

        algorithm = self.ALGORITHMS[algorithm_info['algorithm']]
        algorithm_info.update(algorithm)

        return algorithm_info
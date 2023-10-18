def _sign_data(self, data, options):
        '''Add signature to data'''

        if options['signature_algorithm_id'] not in self.signature_algorithms:
            raise Exception('Unknown signature algorithm id: %d'
                            % options['signature_algorithm_id'])

        signature_algorithm = \
            self.signature_algorithms[options['signature_algorithm_id']]

        algorithm = self._get_algorithm_info(signature_algorithm)

        key_salt = get_random_bytes(algorithm['salt_size'])
        key = self._generate_key(options['signature_passphrase_id'],
                            self.signature_passphrases, key_salt, algorithm)

        data = self._encode(data, algorithm, key)

        return data + key_salt
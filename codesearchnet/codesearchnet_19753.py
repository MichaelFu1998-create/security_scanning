def _encrypt_data(self, data, options):
        '''Encrypt data'''

        if options['encryption_algorithm_id'] not in self.encryption_algorithms:
            raise Exception('Unknown encryption algorithm id: %d'
                            % options['encryption_algorithm_id'])

        encryption_algorithm = \
            self.encryption_algorithms[options['encryption_algorithm_id']]

        algorithm = self._get_algorithm_info(encryption_algorithm)

        key_salt = get_random_bytes(algorithm['salt_size'])
        key = self._generate_key(options['encryption_passphrase_id'],
                            self.encryption_passphrases, key_salt, algorithm)

        data = self._encode(data, algorithm, key)

        return data + key_salt
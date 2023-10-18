def _decrypt_data(self, data, options):
        '''Decrypt data'''

        if options['encryption_algorithm_id'] not in self.encryption_algorithms:
            raise Exception('Unknown encryption algorithm id: %d'
                            % options['encryption_algorithm_id'])

        encryption_algorithm = \
            self.encryption_algorithms[options['encryption_algorithm_id']]

        algorithm = self._get_algorithm_info(encryption_algorithm)

        key_salt = ''
        if algorithm['salt_size']:
            key_salt = data[-algorithm['salt_size']:]
            data = data[:-algorithm['salt_size']]

        key = self._generate_key(options['encryption_passphrase_id'],
                            self.encryption_passphrases, key_salt, algorithm)

        data = self._decode(data, algorithm, key)

        return data
def _generate_key(pass_id, passphrases, salt, algorithm):
        '''Generate and return PBKDF2 key'''

        if pass_id not in passphrases:
            raise Exception('Passphrase not defined for id: %d' % pass_id)

        passphrase = passphrases[pass_id]

        if len(passphrase) < 32:
            raise Exception('Passphrase less than 32 characters long')

        digestmod = EncryptedPickle._get_hashlib(algorithm['pbkdf2_algorithm'])

        encoder = PBKDF2(passphrase, salt,
                         iterations=algorithm['pbkdf2_iterations'],
                         digestmodule=digestmod)

        return encoder.read(algorithm['key_size'])
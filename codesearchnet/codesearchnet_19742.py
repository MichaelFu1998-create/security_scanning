def set_algorithms(self, signature=None, encryption=None,
                       serialization=None, compression=None):
        '''Set algorithms used for sealing. Defaults can not be overridden.'''

        self.signature_algorithms = \
            self._update_dict(signature, self.DEFAULT_SIGNATURE)

        self.encryption_algorithms = \
            self._update_dict(encryption, self.DEFAULT_ENCRYPTION)

        self.serialization_algorithms = \
            self._update_dict(serialization, self.DEFAULT_SERIALIZATION)

        self.compression_algorithms = \
            self._update_dict(compression, self.DEFAULT_COMPRESSION)
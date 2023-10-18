def get_algorithms(self):
        '''Get algorithms used for sealing'''

        return {
            'signature': self.signature_algorithms,
            'encryption': self.encryption_algorithms,
            'serialization': self.serialization_algorithms,
            'compression': self.compression_algorithms,
        }
def set_signature_passphrases(self, signature_passphrases):
        '''Set signature passphrases'''
        self.signature_passphrases = self._update_dict(signature_passphrases,
                                                       {}, replace_data=True)
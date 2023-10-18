def set_encryption_passphrases(self, encryption_passphrases):
        '''Set encryption passphrases'''
        self.encryption_passphrases = self._update_dict(encryption_passphrases,
                                                        {}, replace_data=True)
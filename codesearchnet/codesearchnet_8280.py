def decrypt(self, wif):
        """ Decrypt the content according to BIP38

            :param str wif: Encrypted key
        """
        if not self.unlocked():
            raise WalletLocked
        return format(bip38.decrypt(wif, self.masterkey), "wif")
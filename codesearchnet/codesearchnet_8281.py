def encrypt(self, wif):
        """ Encrypt the content according to BIP38

            :param str wif: Unencrypted key
        """
        if not self.unlocked():
            raise WalletLocked
        return format(bip38.encrypt(str(wif), self.masterkey), "encwif")
def appendWif(self, wif):
        """ Add a wif that should be used for signing of the transaction.
        """
        if wif:
            try:
                self.privatekey_class(wif)
                self.wifs.add(wif)
            except Exception:
                raise InvalidWifError
def appendMissingSignatures(self):
        """ Store which accounts/keys are supposed to sign the transaction

            This method is used for an offline-signer!
        """
        missing_signatures = self.get("missing_signatures", [])
        for pub in missing_signatures:
            wif = self.blockchain.wallet.getPrivateKeyForPublicKey(pub)
            if wif:
                self.appendWif(wif)
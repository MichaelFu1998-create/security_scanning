def update_cer(self, cer, account=None, **kwargs):
        """ Update the Core Exchange Rate (CER) of an asset
        """
        assert callable(self.blockchain.update_cer)
        return self.blockchain.update_cer(
            self["symbol"], cer, account=account, **kwargs
        )
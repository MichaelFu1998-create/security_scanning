def unlock_wallet(self, *args, **kwargs):
        """ Unlock the library internal wallet
        """
        self.blockchain.wallet.unlock(*args, **kwargs)
        return self
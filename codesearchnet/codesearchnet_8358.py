def getActiveKeyForAccount(self, name):
        """ Obtain owner Active Key for an account from the wallet database
        """
        account = self.rpc.get_account(name)
        for authority in account["active"]["key_auths"]:
            try:
                return self.getPrivateKeyForPublicKey(authority[0])
            except Exception:
                pass
        return False
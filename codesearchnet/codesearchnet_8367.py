def encrypt(self, message):
        """ Encrypt a memo

            :param str message: clear text memo message
            :returns: encrypted message
            :rtype: str
        """
        if not message:
            return None

        nonce = str(random.getrandbits(64))
        try:
            memo_wif = self.blockchain.wallet.getPrivateKeyForPublicKey(
                self.from_account["options"]["memo_key"]
            )
        except KeyNotFound:
            # if all fails, raise exception
            raise MissingKeyError(
                "Memo private key {} for {} could not be found".format(
                    self.from_account["options"]["memo_key"], self.from_account["name"]
                )
            )
        if not memo_wif:
            raise MissingKeyError(
                "Memo key for %s missing!" % self.from_account["name"]
            )

        if not hasattr(self, "chain_prefix"):
            self.chain_prefix = self.blockchain.prefix

        enc = memo.encode_memo(
            self.privatekey_class(memo_wif),
            self.publickey_class(
                self.to_account["options"]["memo_key"], prefix=self.chain_prefix
            ),
            nonce,
            message,
        )

        return {
            "message": enc,
            "nonce": nonce,
            "from": self.from_account["options"]["memo_key"],
            "to": self.to_account["options"]["memo_key"],
        }
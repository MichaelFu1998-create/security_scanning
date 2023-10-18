def decrypt(self, message):
        """ Decrypt a message

            :param dict message: encrypted memo message
            :returns: decrypted message
            :rtype: str
        """
        if not message:
            return None

        # We first try to decode assuming we received the memo
        try:
            memo_wif = self.blockchain.wallet.getPrivateKeyForPublicKey(message["to"])
            pubkey = message["from"]
        except KeyNotFound:
            try:
                # if that failed, we assume that we have sent the memo
                memo_wif = self.blockchain.wallet.getPrivateKeyForPublicKey(
                    message["from"]
                )
                pubkey = message["to"]
            except KeyNotFound:
                # if all fails, raise exception
                raise MissingKeyError(
                    "None of the required memo keys are installed!"
                    "Need any of {}".format([message["to"], message["from"]])
                )

        if not hasattr(self, "chain_prefix"):
            self.chain_prefix = self.blockchain.prefix

        return memo.decode_memo(
            self.privatekey_class(memo_wif),
            self.publickey_class(pubkey, prefix=self.chain_prefix),
            message.get("nonce"),
            message.get("message"),
        )
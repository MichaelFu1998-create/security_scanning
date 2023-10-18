def sign(self, account=None, **kwargs):
        """ Sign a message with an account's memo key

            :param str account: (optional) the account that owns the bet
                (defaults to ``default_account``)
            :raises ValueError: If not account for signing is provided

            :returns: the signed message encapsulated in a known format
        """
        if not account:
            if "default_account" in self.blockchain.config:
                account = self.blockchain.config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        # Data for message
        account = self.account_class(account, blockchain_instance=self.blockchain)
        info = self.blockchain.info()
        meta = dict(
            timestamp=info["time"],
            block=info["head_block_number"],
            memokey=account["options"]["memo_key"],
            account=account["name"],
        )

        # wif key
        wif = self.blockchain.wallet.getPrivateKeyForPublicKey(
            account["options"]["memo_key"]
        )

        # We strip the message here so we know for sure there are no trailing
        # whitespaces or returns
        message = self.message.strip()

        enc_message = self.SIGNED_MESSAGE_META.format(**locals())

        # signature
        signature = hexlify(sign_message(enc_message, wif)).decode("ascii")

        self.signed_by_account = account
        self.signed_by_name = account["name"]
        self.meta = meta
        self.plain_message = message

        return self.SIGNED_MESSAGE_ENCAPSULATED.format(
            MESSAGE_SPLIT=self.MESSAGE_SPLIT, **locals()
        )
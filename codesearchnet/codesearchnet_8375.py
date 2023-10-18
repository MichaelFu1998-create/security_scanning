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

        # wif key
        wif = self.blockchain.wallet.getPrivateKeyForPublicKey(
            account["options"]["memo_key"]
        )

        payload = [
            "from",
            account["name"],
            "key",
            account["options"]["memo_key"],
            "time",
            str(datetime.utcnow()),
            "text",
            self.message,
        ]
        enc_message = json.dumps(payload, separators=(",", ":"))

        # signature
        signature = hexlify(sign_message(enc_message, wif)).decode("ascii")

        return dict(signed=enc_message, payload=payload, signature=signature)
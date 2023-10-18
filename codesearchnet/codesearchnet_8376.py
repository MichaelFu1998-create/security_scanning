def verify(self, **kwargs):
        """ Verify a message with an account's memo key

            :param str account: (optional) the account that owns the bet
                (defaults to ``default_account``)

            :returns: True if the message is verified successfully
            :raises InvalidMessageSignature if the signature is not ok
        """
        if not isinstance(self.message, dict):
            try:
                self.message = json.loads(self.message)
            except Exception:
                raise ValueError("Message must be valid JSON")

        payload = self.message.get("payload")
        assert payload, "Missing payload"
        payload_dict = {k[0]: k[1] for k in zip(payload[::2], payload[1::2])}
        signature = self.message.get("signature")

        account_name = payload_dict.get("from").strip()
        memo_key = payload_dict.get("key").strip()

        assert account_name, "Missing account name 'from'"
        assert memo_key, "missing 'key'"

        try:
            self.publickey_class(memo_key, prefix=self.blockchain.prefix)
        except Exception:
            raise InvalidMemoKeyException("The memo key in the message is invalid")

        # Load account from blockchain
        try:
            account = self.account_class(
                account_name, blockchain_instance=self.blockchain
            )
        except AccountDoesNotExistsException:
            raise AccountDoesNotExistsException(
                "Could not find account {}. Are you connected to the right chain?".format(
                    account_name
                )
            )

        # Test if memo key is the same as on the blockchain
        if not account["options"]["memo_key"] == memo_key:
            raise WrongMemoKey(
                "Memo Key of account {} on the Blockchain ".format(account["name"])
                + "differs from memo key in the message: {} != {}".format(
                    account["options"]["memo_key"], memo_key
                )
            )

        # Ensure payload and signed match
        signed_target = json.dumps(self.message.get("payload"), separators=(",", ":"))
        signed_actual = self.message.get("signed")
        assert (
            signed_target == signed_actual
        ), "payload doesn't match signed message: \n{}\n{}".format(
            signed_target, signed_actual
        )

        # Reformat message
        enc_message = self.message.get("signed")

        # Verify Signature
        pubkey = verify_message(enc_message, unhexlify(signature))

        # Verify pubky
        pk = self.publickey_class(
            hexlify(pubkey).decode("ascii"), prefix=self.blockchain.prefix
        )
        if format(pk, self.blockchain.prefix) != memo_key:
            raise InvalidMessageSignature("The signature doesn't match the memo key")

        self.signed_by_account = account
        self.signed_by_name = account["name"]
        self.plain_message = payload_dict.get("text")

        return True
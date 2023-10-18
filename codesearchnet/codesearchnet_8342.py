def sign(self, wifkeys, chain=None):
        """ Sign the transaction with the provided private keys.

            :param array wifkeys: Array of wif keys
            :param str chain: identifier for the chain

        """
        if not chain:
            chain = self.get_default_prefix()
        self.deriveDigest(chain)

        # Get Unique private keys
        self.privkeys = []
        for item in wifkeys:
            if item not in self.privkeys:
                self.privkeys.append(item)

        # Sign the message with every private key given!
        sigs = []
        for wif in self.privkeys:
            signature = sign_message(self.message, wif)
            sigs.append(Signature(signature))

        self.data["signatures"] = Array(sigs)
        return self
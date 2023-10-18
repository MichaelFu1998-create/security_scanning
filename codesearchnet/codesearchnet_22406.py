def broadcast_tx(self, address, amount, secret, secondsecret=None, vendorfield=''):
        """broadcasts a transaction to the peerslist using ark-js library"""

        peer = random.choice(self.PEERS)
        park = Park(
            peer,
            4001,
            constants.ARK_NETHASH,
            '1.1.1'
        )

        return park.transactions().create(address, str(amount), vendorfield, secret, secondsecret)
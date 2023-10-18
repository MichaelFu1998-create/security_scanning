def public_address(self, net='mainnet'):
        """Returns the master :class:`Address <monero.address.Address>` represented by the seed.

        :param net: the network, one of 'mainnet', 'testnet', 'stagenet'. Default is 'mainnet'.

        :rtype: :class:`Address <monero.address.Address>`
        """
        if net not in ('mainnet', 'testnet', 'stagenet'):
            raise ValueError(
                "Invalid net argument. Must be one of ('mainnet', 'testnet', 'stagenet').")
        netbyte = 18 if net == 'mainnet' else 53 if net == 'testnet' else 24
        data = "{:x}{:s}{:s}".format(netbyte, self.public_spend_key(), self.public_view_key())
        h = keccak_256()
        h.update(unhexlify(data))
        checksum = h.hexdigest()
        return address(base58.encode(data + checksum[0:8]))
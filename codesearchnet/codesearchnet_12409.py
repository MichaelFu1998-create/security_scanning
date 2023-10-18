def get_address(self, major, minor):
        """
        Calculates sub-address for account index (`major`) and address index within
        the account (`minor`).

        :rtype: :class:`BaseAddress <monero.address.BaseAddress>`
        """
        # ensure indexes are within uint32
        if major < 0 or major >= 2**32:
            raise ValueError('major index {} is outside uint32 range'.format(major))
        if minor < 0 or minor >= 2**32:
            raise ValueError('minor index {} is outside uint32 range'.format(minor))
        master_address = self.address()
        if major == minor == 0:
            return master_address
        master_svk = unhexlify(self.view_key())
        master_psk = unhexlify(self.address().spend_key())
        # m = Hs("SubAddr\0" || master_svk || major || minor)
        hsdata = b''.join([
                b'SubAddr\0', master_svk,
                struct.pack('<I', major), struct.pack('<I', minor)])
        m = keccak_256(hsdata).digest()
        # D = master_psk + m * B
        D = ed25519.add_compressed(
                ed25519.decodepoint(master_psk),
                ed25519.scalarmult(ed25519.B, ed25519.decodeint(m)))
        # C = master_svk * D
        C = ed25519.scalarmult(D, ed25519.decodeint(master_svk))
        netbyte = bytearray([
                42 if master_address.is_mainnet() else \
                63 if master_address.is_testnet() else 36])
        data = netbyte + ed25519.encodepoint(D) + ed25519.encodepoint(C)
        checksum = keccak_256(data).digest()[:4]
        return address.SubAddress(base58.encode(hexlify(data + checksum)))
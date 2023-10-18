def create_account(self, address=None, balance=0, code=None, storage=None, nonce=None):
        """
        Low level account creation. No transaction is done.
        :param address: the address of the account, if known. If omitted, a new address will be generated as closely to the Yellow Paper as possible.
        :param balance: the initial balance of the account in Wei
        :param code: the runtime code of the account, if a contract
        :param storage: storage array
        :param nonce: the nonce for the account; contracts should have a nonce greater than or equal to 1
        """
        if code is None:
            code = bytes()
        else:
            if not isinstance(code, (bytes, Array)):
                raise EthereumError('Wrong code type')

        # nonce default to initial nonce
        if nonce is None:
            # As per EIP 161, contract accounts are initialized with a nonce of 1
            nonce = 1 if code else 0

        if address is None:
            address = self.new_address()

        if not isinstance(address, int):
            raise EthereumError('You must provide an address')

        if address in self.accounts:
            # FIXME account may have been created via selfdestruct destination
            # or CALL and may contain some ether already, though if it was a
            # selfdestructed address, it can not be reused
            raise EthereumError('The account already exists')

        if storage is None:
            # Uninitialized values in a storage are 0 by spec
            storage = self.constraints.new_array(index_bits=256, value_bits=256, name=f'STORAGE_{address:x}', avoid_collisions=True, default=0)
        else:
            if isinstance(storage, ArrayProxy):
                if storage.index_bits != 256 or storage.value_bits != 256:
                    raise TypeError("An ArrayProxy 256bits -> 256bits is needed")
            else:
                if any((k < 0 or k >= 1 << 256 for k, v in storage.items())):
                    raise TypeError("Need a dict like object that maps 256 bits keys to 256 bits values")
            # Hopefully here we have a mapping from 256b to 256b

        self._world_state[address] = {}
        self._world_state[address]['nonce'] = nonce
        self._world_state[address]['balance'] = balance
        self._world_state[address]['storage'] = storage
        self._world_state[address]['code'] = code

        # adds hash of new address
        data = binascii.unhexlify('{:064x}{:064x}'.format(address, 0))
        value = sha3.keccak_256(data).hexdigest()
        value = int(value, 16)
        self._publish('on_concrete_sha3', data, value)

        return address
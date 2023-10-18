def create_contract(self, price=0, address=None, caller=None, balance=0, init=None, gas=None):
        """
        Create a contract account. Sends a transaction to initialize the contract

        :param address: the address of the new account, if known. If omitted, a new address will be generated as closely to the Yellow Paper as possible.
        :param balance: the initial balance of the account in Wei
        :param init: the initialization code of the contract

        The way that the Solidity compiler expects the constructor arguments to
        be passed is by appending the arguments to the byte code produced by the
        Solidity compiler. The arguments are formatted as defined in the Ethereum
        ABI2. The arguments are then copied from the init byte array to the EVM
        memory through the CODECOPY opcode with appropriate values on the stack.
        This is done when the byte code in the init byte array is actually run
        on the network.
        """
        expected_address = self.create_account(self.new_address(sender=caller))
        if address is None:
            address = expected_address
        elif caller is not None and address != expected_address:
            raise EthereumError(f"Error: contract created from address {hex(caller)} with nonce {self.get_nonce(caller)} was expected to be at address {hex(expected_address)}, but create_contract was called with address={hex(address)}")
        self.start_transaction('CREATE', address, price, init, caller, balance, gas=gas)
        self._process_pending_transaction()
        return address
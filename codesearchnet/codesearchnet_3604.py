def CREATE(self, value, offset, size):
        """Create a new account with associated code"""
        address = self.world.create_account(address=EVMWorld.calculate_new_address(sender=self.address, nonce=self.world.get_nonce(self.address)))
        self.world.start_transaction('CREATE',
                                     address,
                                     data=self.read_buffer(offset, size),
                                     caller=self.address,
                                     value=value,
                                     gas=self.gas)

        raise StartTx()
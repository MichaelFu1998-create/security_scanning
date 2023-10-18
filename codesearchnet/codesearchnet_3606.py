def CALLCODE(self, gas, _ignored_, value, in_offset, in_size, out_offset, out_size):
        """Message-call into this account with alternative account's code"""
        self.world.start_transaction('CALLCODE',
                                     address=self.address,
                                     data=self.read_buffer(in_offset, in_size),
                                     caller=self.address,
                                     value=value,
                                     gas=gas)
        raise StartTx()
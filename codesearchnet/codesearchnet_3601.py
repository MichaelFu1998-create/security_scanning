def SSTORE(self, offset, value):
        """Save word to storage"""
        storage_address = self.address
        self._publish('will_evm_write_storage', storage_address, offset, value)
        #refund = Operators.ITEBV(256,
        #                         previous_value != 0,
        #                         Operators.ITEBV(256, value != 0, 0, GSTORAGEREFUND),
        #                         0)

        if istainted(self.pc):
            for taint in get_taints(self.pc):
                value = taint_with(value, taint)
        self.world.set_storage_data(storage_address, offset, value)
        self._publish('did_evm_write_storage', storage_address, offset, value)
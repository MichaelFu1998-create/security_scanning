def SLOAD(self, offset):
        """Load word from storage"""
        storage_address = self.address
        self._publish('will_evm_read_storage', storage_address, offset)
        value = self.world.get_storage_data(storage_address, offset)
        self._publish('did_evm_read_storage', storage_address, offset, value)
        return value
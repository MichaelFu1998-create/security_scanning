def CREATE(self, value, offset, size):
        """Create a new account with associated code"""
        tx = self.world.last_transaction  # At this point last and current tx are the same.
        address = tx.address
        if tx.result == 'RETURN':
            self.world.set_code(tx.address, tx.return_data)
        else:
            self.world.delete_account(address)
            address = 0
        return address
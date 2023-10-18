def new_address(self, sender=None, nonce=None):
        """Create a fresh 160bit address"""
        if sender is not None and nonce is None:
            nonce = self.get_nonce(sender)

        new_address = self.calculate_new_address(sender, nonce)
        if sender is None and new_address in self:
            return self.new_address(sender, nonce)
        return new_address
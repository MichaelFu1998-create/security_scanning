def SELFDESTRUCT(self, recipient):
        """Halt execution and register account for later deletion"""
        #This may create a user account
        recipient = Operators.EXTRACT(recipient, 0, 160)
        address = self.address
        #FIXME for on the known addresses
        if issymbolic(recipient):
            logger.info("Symbolic recipient on self destruct")
            recipient = solver.get_value(self.constraints, recipient)

        if recipient not in self.world:
            self.world.create_account(address=recipient)

        self.world.send_funds(address, recipient, self.world.get_balance(address))
        self.world.delete_account(address)

        raise EndTx('SELFDESTRUCT')
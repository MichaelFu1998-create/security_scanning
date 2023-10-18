def balance(address):
        """
        Takes a single address and returns the current balance.
        """
        txhistory = Address.transactions(address)
        balance = 0
        for i in txhistory:
            if i.recipientId == address:
                balance += i.amount
            if i.senderId == address:
                balance -= (i.amount + i.fee)

        delegates = Delegate.delegates()
        for i in delegates:
            if address == i.address:
                forged_blocks = Delegate.blocks(i.pubkey)
                for block in forged_blocks:
                    balance += (block.reward + block.totalFee)

        if balance < 0:
            height = Node.height()
            logger.fatal('Negative balance for address {0}, Nodeheight: {1)'.format(address, height))
            raise NegativeBalanceError('Negative balance for address {0}, Nodeheight: {1)'.format(address, height))
        return balance
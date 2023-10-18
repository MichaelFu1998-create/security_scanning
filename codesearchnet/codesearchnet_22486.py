def balance_over_time(address):
        """returns a list of named tuples,  x.timestamp, x.amount including block rewards"""
        forged_blocks = None
        txhistory = Address.transactions(address)
        delegates = Delegate.delegates()
        for i in delegates:
            if address == i.address:
                forged_blocks = Delegate.blocks(i.pubkey)

        balance_over_time = []
        balance = 0
        block = 0

        Balance = namedtuple(
            'balance',
            'timestamp amount')

        for tx in txhistory:
            if forged_blocks:
                while forged_blocks[block].timestamp <= tx.timestamp:
                    balance += (forged_blocks[block].reward + forged_blocks[block].totalFee)
                    balance_over_time.append(Balance(timestamp=forged_blocks[block].timestamp, amount=balance))
                    block += 1

            if tx.senderId == address:
                balance -= (tx.amount + tx.fee)
                res = Balance(timestamp=tx.timestamp, amount=balance)
                balance_over_time.append(res)
            if tx.recipientId == address:
                balance += tx.amount
                res = Balance(timestamp=tx.timestamp, amount=balance)
                balance_over_time.append(res)

        if forged_blocks and block <= len(forged_blocks) - 1:
            if forged_blocks[block].timestamp > txhistory[-1].timestamp:
                for i in forged_blocks[block:]:
                    balance += (i.reward + i.totalFee)
                    res = Balance(timestamp=i.timestamp, amount=balance)
                    balance_over_time.append(res)

        return balance_over_time
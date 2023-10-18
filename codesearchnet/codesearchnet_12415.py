def transfer_multiple(self, destinations,
            priority=prio.NORMAL, payment_id=None, unlock_time=0,
            relay=True):
        """
        Sends a batch of transfers. Returns a list of resulting transactions.

        :param destinations: a list of destination and amount pairs:
                    [(:class:`Address <monero.address.Address>`, `Decimal`), ...]
        :param priority: transaction priority, implies fee. The priority can be a number
                    from 1 to 4 (unimportant, normal, elevated, priority) or a constant
                    from `monero.prio`.
        :param payment_id: ID for the payment (must be None if
                        :class:`IntegratedAddress <monero.address.IntegratedAddress>`
                        is used as the destination)
        :param unlock_time: the extra unlock delay
        :param relay: if `True`, the wallet will relay the transaction(s) to the network
                        immediately; when `False`, it will only return the transaction(s)
                        so they might be broadcasted later
        :rtype: list of :class:`Transaction <monero.transaction.Transaction>`
        """
        return self._backend.transfer(
            destinations,
            priority,
            payment_id,
            unlock_time,
            account=self.index,
            relay=relay)
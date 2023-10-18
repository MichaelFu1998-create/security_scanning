def confirmations(self, txn_or_pmt):
        """
        Returns the number of confirmations for given
        :class:`Transaction <monero.transaction.Transaction>` or
        :class:`Payment <monero.transaction.Payment>` object.

        :rtype: int
        """
        if isinstance(txn_or_pmt, Payment):
            txn = txn_or_pmt.transaction
        else:
            txn = txn_or_pmt
        try:
            return max(0, self.height() - txn.height)
        except TypeError:
            return 0
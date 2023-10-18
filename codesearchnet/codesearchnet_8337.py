def broadcast(self, tx=None):
        """ Broadcast a transaction to the Blockchain

            :param tx tx: Signed transaction to broadcast
        """
        if tx:
            # If tx is provided, we broadcast the tx
            return self.transactionbuilder_class(
                tx, blockchain_instance=self
            ).broadcast()
        else:
            return self.txbuffer.broadcast()
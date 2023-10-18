def awaitTxConfirmation(self, transaction, limit=10):
        """ Returns the transaction as seen by the blockchain after being
            included into a block

            .. note:: If you want instant confirmation, you need to instantiate
                      class:`.blockchain.Blockchain` with
                      ``mode="head"``, otherwise, the call will wait until
                      confirmed in an irreversible block.

            .. note:: This method returns once the blockchain has included a
                      transaction with the **same signature**. Even though the
                      signature is not usually used to identify a transaction,
                      it still cannot be forfeited and is derived from the
                      transaction contented and thus identifies a transaction
                      uniquely.
        """
        counter = 10
        for block in self.blocks():
            counter += 1
            for tx in block["transactions"]:
                if sorted(tx["signatures"]) == sorted(transaction["signatures"]):
                    return tx
            if counter > limit:
                raise Exception("The operation has not been added after 10 blocks!")
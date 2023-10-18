def broadcast(self):
        """ Broadcast a transaction to the blockchain network

            :param tx tx: Signed transaction to broadcast
        """
        # Sign if not signed
        if not self._is_signed():
            self.sign()

        # Cannot broadcast an empty transaction
        if "operations" not in self or not self["operations"]:
            log.warning("No operations in transaction! Returning")
            return

        # Obtain JS
        ret = self.json()

        # Debugging mode does not broadcast
        if self.blockchain.nobroadcast:
            log.warning("Not broadcasting anything!")
            self.clear()
            return ret

        # Broadcast
        try:
            if self.blockchain.blocking:
                ret = self.blockchain.rpc.broadcast_transaction_synchronous(
                    ret, api="network_broadcast"
                )
                ret.update(**ret.get("trx", {}))
            else:
                self.blockchain.rpc.broadcast_transaction(ret, api="network_broadcast")
        except Exception as e:
            raise e
        finally:
            self.clear()

        return ret
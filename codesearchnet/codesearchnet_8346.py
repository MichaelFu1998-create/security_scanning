def refresh(self):
        """ This is the refresh method that overloads the prototype in
            BlockchainObject.
        """
        dict.__init__(
            self,
            self.blockchain.rpc.get_object(self.identifier),
            blockchain_instance=self.blockchain,
        )
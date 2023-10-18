def new_tx(self, *args, **kwargs):
        """ Let's obtain a new txbuffer

            :returns int txid: id of the new txbuffer
        """
        builder = self.transactionbuilder_class(
            *args, blockchain_instance=self, **kwargs
        )
        self._txbuffers.append(builder)
        return builder
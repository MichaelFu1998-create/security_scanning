def check_confirmations_or_resend(self, use_open_peers=False, **kw):
        """
        check if a tx is confirmed, else resend it.

        :param use_open_peers: select random peers fro api/peers endpoint
        """
        if self.confirmations() == 0:
            self.send(use_open_peers, **kw)
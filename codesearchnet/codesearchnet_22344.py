def send(self, use_open_peers=True, queue=True, **kw):
        """
        send a transaction immediately. Failed transactions are picked up by the TxBroadcaster

        :param ip: specific peer IP to send tx to
        :param port: port of specific peer
        :param use_open_peers: use Arky's broadcast method
        """

        if not use_open_peers:
            ip = kw.get('ip')
            port = kw.get('port')
            peer = 'http://{}:{}'.format(ip, port)
            res = arky.rest.POST.peer.transactions(peer=peer, transactions=[self.tx.tx])

        else:
            res = arky.core.sendPayload(self.tx.tx)

        if self.tx.success != '0.0%':
            self.tx.error = None
            self.tx.success = True
        else:
            self.tx.error = res['messages']
            self.tx.success = False

        self.tx.tries += 1
        self.tx.res = res

        if queue:
            self.tx.send = True

        self.__save()
        return res
def remove_peer(self, peer):
        """
        remove one or multiple peers from PEERS variable

        :param peer(list or string):
        """
        if type(peer) == list:
            for x in peer:
                check_url(x)
                for i in self.PEERS:
                    if x in i:
                        self.PEERS.remove(i)
        elif type(peer) == str:
            check_url(peer)
            for i in self.PEERS:
                if peer == i:
                    self.PEERS.remove(i)
        else:
            raise ValueError('peer paramater did not pass url validation')
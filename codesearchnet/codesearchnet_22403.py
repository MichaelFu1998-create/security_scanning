def add_peer(self, peer):
        """
        Add a peer or multiple peers to the PEERS variable, takes a single string or a list.

        :param peer(list or string)
        """
        if type(peer) == list:
            for i in peer:
                check_url(i)
            self.PEERS.extend(peer)
        elif type(peer) == str:
            check_url(peer)
            self.PEERS.append(peer)
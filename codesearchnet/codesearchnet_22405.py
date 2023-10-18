def status(self):
        """
        check the status of the network and the peers

        :return: network_height, peer_status
        """
        peer = random.choice(self.PEERS)
        formatted_peer = 'http://{}:4001'.format(peer)
        peerdata = requests.get(url=formatted_peer + '/api/peers/').json()['peers']
        peers_status = {}

        networkheight = max([x['height'] for x in peerdata])

        for i in peerdata:
            if 'http://{}:4001'.format(i['ip']) in self.PEERS:
                peers_status.update({i['ip']: {
                    'height': i['height'],
                    'status': i['status'],
                    'version': i['version'],
                    'delay': i['delay'],
                }})

        return {
            'network_height': networkheight,
            'peer_status': peers_status
        }
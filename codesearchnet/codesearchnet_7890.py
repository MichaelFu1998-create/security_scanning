def send_packet(self, pkt):
        """Low-level interface to queue a packet on the wire (encoded as wire
        protocol"""
        self.put_client_msg(packet.encode(pkt, self.json_dumps))
def update_received_packet(self, received_pkt_size_bytes):
    """Update received packet metrics"""
    self.update_count(self.RECEIVED_PKT_COUNT)
    self.update_count(self.RECEIVED_PKT_SIZE, incr_by=received_pkt_size_bytes)
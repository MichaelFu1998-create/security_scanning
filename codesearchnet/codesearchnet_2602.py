def update_sent_packet(self, sent_pkt_size_bytes):
    """Update sent packet metrics"""
    self.update_count(self.SENT_PKT_COUNT)
    self.update_count(self.SENT_PKT_SIZE, incr_by=sent_pkt_size_bytes)
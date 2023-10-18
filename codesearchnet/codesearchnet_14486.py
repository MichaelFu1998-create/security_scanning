def push(self, ip_packet):
        """ push the packet into the queue """

        data_len = len(ip_packet.data.data)
        seq_id = ip_packet.data.seq

        if data_len == 0:
            self._next_seq_id = seq_id
            return False

        # have we seen this packet?
        if self._next_seq_id != -1 and seq_id != self._next_seq_id:
            return False

        self._next_seq_id = seq_id + data_len

        with self._lock_packets:
            # Note: we only account for payload (i.e.: tcp data)
            self._length += len(ip_packet.data.data)
            self._remaining += len(ip_packet.data.data)

            self._packets.append(ip_packet)

        return True
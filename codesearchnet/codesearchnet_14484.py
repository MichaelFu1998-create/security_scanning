def pop(self, nbytes):
        """ pops packets with _at least_ nbytes of payload """
        size = 0
        popped = []
        with self._lock_packets:
            while size < nbytes:
                try:
                    packet = self._packets.pop(0)
                    size += len(packet.data.data)
                    self._remaining -= len(packet.data.data)
                    popped.append(packet)
                except IndexError:
                    break
        return popped
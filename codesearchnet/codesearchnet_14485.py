def pop_data(self, nbytes):
        """ similar to pop, but returns payload + last timestamp """
        last_timestamp = 0
        data = []
        for packet in self.pop(nbytes):
            last_timestamp = packet.timestamp
            data.append(packet.data.data)

        return ''.join(data), last_timestamp
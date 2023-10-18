def send_packet(self, data):
        """SHOULD BE PRIVATE"""
        package_size = 4032  # bit smaller than 4096 because of headers
        for i in range(int(math.ceil(len(data) / package_size))):
            start = i * package_size
            end = (i + 1) * package_size
            self._spi.write(data[start:end])
            self._spi.flush()
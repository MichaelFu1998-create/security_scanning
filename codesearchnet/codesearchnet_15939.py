def strip_rate(self, idx):
        """strip(1 byte) radiotap.datarate
        note that, unit of this field is originally 0.5 Mbps
        :idx: int
        :return: int
            idx
        :return: double
            rate in terms of Mbps
        """
        val, = struct.unpack_from('<B', self._rtap, idx)
        rate_unit = float(1) / 2    # Mbps
        return idx + 1, rate_unit * val
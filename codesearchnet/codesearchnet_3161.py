def _raw_read(self, where: int, size=1) -> bytes:
        """
        Selects bytes from memory. Attempts to do so faster than via read_bytes.

        :param where: address to read from
        :param size: number of bytes to read
        :return: the bytes in memory
        """
        map = self.memory.map_containing(where)
        start = map._get_offset(where)
        mapType = type(map)
        if mapType is FileMap:
            end = map._get_offset(where + size)

            if end > map._mapped_size:
                logger.warning(f"Missing {end - map._mapped_size} bytes at the end of {map._filename}")

            raw_data = map._data[map._get_offset(where): min(end, map._mapped_size)]
            if len(raw_data) < end:
                raw_data += b'\x00' * (end - len(raw_data))

            data = b''
            for offset in sorted(map._overlay.keys()):
                data += raw_data[len(data):offset]
                data += map._overlay[offset]
            data += raw_data[len(data):]

        elif mapType is AnonMap:
            data = bytes(map._data[start:start + size])
        else:
            data = b''.join(self.memory[where:where + size])
        assert len(data) == size, 'Raw read resulted in wrong data read which should never happen'
        return data
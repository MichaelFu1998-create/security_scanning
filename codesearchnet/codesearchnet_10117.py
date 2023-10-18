def read_until(self, marker):
        """
        Reads data from the socket until a marker is found. Data read includes
        the marker.

        :param marker:
            A byte string or regex object from re.compile(). Used to determine
            when to stop reading. Regex objects are more inefficient since
            they must scan the entire byte string of read data each time data
            is read off the socket.

        :return:
            A byte string of the data read, including the marker
        """

        if not isinstance(marker, byte_cls) and not isinstance(marker, Pattern):
            raise TypeError(pretty_message(
                '''
                marker must be a byte string or compiled regex object, not %s
                ''',
                type_name(marker)
            ))

        output = b''

        is_regex = isinstance(marker, Pattern)

        while True:
            if len(self._decrypted_bytes) > 0:
                chunk = self._decrypted_bytes
                self._decrypted_bytes = b''
            else:
                to_read = self._os_buffered_size() or 8192
                chunk = self.read(to_read)

            offset = len(output)
            output += chunk

            if is_regex:
                match = marker.search(output)
                if match is not None:
                    end = match.end()
                    break
            else:
                # If the marker was not found last time, we have to start
                # at a position where the marker would have its final char
                # in the newly read chunk
                start = max(0, offset - len(marker) - 1)
                match = output.find(marker, start)
                if match != -1:
                    end = match + len(marker)
                    break

        self._decrypted_bytes = output[end:] + self._decrypted_bytes
        return output[0:end]
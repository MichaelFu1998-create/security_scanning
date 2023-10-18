def data_received(self, data):
        """ Received from QTM and route accordingly """
        self._received_data += data
        h_size = RTheader.size

        data = self._received_data
        size, type_ = RTheader.unpack_from(data, 0)

        while len(data) >= size:
            self._parse_received(data[h_size:size], type_)
            data = data[size:]

            if len(data) < h_size:
                break

            size, type_ = RTheader.unpack_from(data, 0)

        self._received_data = data
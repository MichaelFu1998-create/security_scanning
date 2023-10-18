def scan_mem(self, data_to_find):
        """
        Scan for concrete bytes in all mapped memory. Successively yield addresses of all matches.

        :param bytes data_to_find: String to locate
        :return:
        """

        # TODO: for the moment we just treat symbolic bytes as bytes that don't match.
        # for our simple test cases right now, the bytes we're interested in scanning
        # for will all just be there concretely
        # TODO: Can probably do something smarter here like Boyer-Moore, but unnecessary
        # if we're looking for short strings.

        # Querying mem with an index returns [bytes]
        if isinstance(data_to_find, bytes):
            data_to_find = [bytes([c]) for c in data_to_find]

        for mapping in sorted(self.maps):
            for ptr in mapping:
                if ptr + len(data_to_find) >= mapping.end:
                    break

                candidate = mapping[ptr:ptr + len(data_to_find)]

                # TODO: treat symbolic bytes as bytes that don't match. for our simple tests right now, the
                # bytes will be there concretely
                if issymbolic(candidate[0]):
                    break

                if candidate == data_to_find:
                    yield ptr
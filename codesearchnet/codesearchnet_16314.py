def _calculate_float(self, byte_array):
        """Returns an IEEE 754 float from an array of 4 bytes

        :param byte_array: Expects an array of 4 bytes

        :type byte_array: array

        :rtype: float
        """
        if len(byte_array) != 4:
            return None

        return struct.unpack('f', struct.pack('4B', *byte_array))[0]
def strip_bitmap_str(payload):
        """strip(8 byte) wlan.ba.bm
        :payload: ctypes.structure
        :return: str
            bitmap
        """
        bitmap = struct.unpack('BBBBBBBB', payload)
        bitmap_str = ''
        for elem in bitmap:
            bitmap_str += format(elem, '08b')[::-1]
        return bitmap_str
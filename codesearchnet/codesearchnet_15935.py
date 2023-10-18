def _strip_rtap(frame):
        """strip injected radiotap header.
        :return: ctypes.Structure
            radiotap header
        :return: ctypes.Structure
            actual layer 2 Wi-Fi payload
        """
        rtap_len = WiHelper.__get_rtap_len(frame)
        rtap = frame[:rtap_len]
        packet = frame[rtap_len:]
        return rtap, packet
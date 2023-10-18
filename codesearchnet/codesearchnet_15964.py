def strip_qos_cntrl(self, idx, prot_type):
        """strip(2 byte) wlan.qos
        :idx: int
        :prot_type: string
            802.11 protocol type(.11ac, .11a, .11n, etc)
        :return: int
            number of processed bytes
        :return: int
            qos priority
        :return: int
            qos bit
        :return: int
            qos acknowledgement
        :return: int
            amsdupresent(aggregated mac service data unit)
        """
        qos_cntrl, = struct.unpack('H', self._packet[idx:idx + 2])
        qos_cntrl_bits = format(qos_cntrl, '016b')[::-1]
        qos_pri = qos_cntrl & 0x000f
        qos_bit = int(qos_cntrl_bits[5])
        qos_ack = int(qos_cntrl_bits[6:8], 2)
        amsdupresent = 0
        if prot_type == '.11ac':
            amsdupresent = int(qos_cntrl_bits[7])
        return 2, qos_pri, qos_bit, qos_ack, amsdupresent
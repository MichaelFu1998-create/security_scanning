def strip_msdu(self, idx):
        """strip single mac servis data unit(msdu)
        see -> https://mrncciew.com/2014/11/01/cwap-802-11-data-frame-aggregation/
        :idx: int
        :return: dict
            msdu
        :return: int
            number of processed bytes
        """
        # length of msdu payload has to be multiple of 4,
        # this guaranteed with padding
        padding = 0
        len_payload = 0
        msdu = {
            'llc': {},
            'wlan.da': None,
            'wlan.sa': None,
            'payload': None,
            'length': 0
        }

        (da_mac, sa_mac) = struct.unpack('!6s6s', self._packet[idx:idx + 12])
        msdu['wlan.da'] = Wifi.get_mac_addr(da_mac)
        msdu['wlan.sa'] = Wifi.get_mac_addr(sa_mac)
        idx += 12
        msdu['length'] = struct.unpack('!H', self._packet[idx:idx + 2])[0]
        idx += 2
        offset, msdu['llc'] = self.strip_llc(idx)
        idx += offset
        len_payload = msdu['length'] - offset
        msdu['payload'] = self._packet[idx:idx + len_payload]
        padding = 4 - (len_payload % 4)
        return msdu, msdu['length'] + padding + 12
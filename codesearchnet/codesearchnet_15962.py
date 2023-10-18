def strip_mac_addrs(self):
        """strip mac address(each 6 byte) information.
        (wlan.ta, wlan.ra, wlan.sa, wlan.da)
        (transmitter, receiver, source, destination)
        :return: int
            index of sequence control
        :return: int
            index after mac addresses
        :return: str
            source address (sa)
        :return: str
            transmitter address (ta)
        :return: str
            receiver address (ra)
        :return: str
            destination address (da)
        :return: str
            basic service sed identifier (bssid)
        """
        qos_idx, seq_idx = 0, 0
        sa, ta, ra, da, bssid = None, None, None, None, None

        if self.to_ds == 1 and self.from_ds == 1:
            (ra, ta, da) = struct.unpack('!6s6s6s', self._packet[4:22])
            sa = struct.unpack('!6s', self._packet[24:30])[0]
            qos_idx = 30
            seq_idx = 22
        elif self.to_ds == 0 and self.from_ds == 1:
            (ra, ta, sa) = struct.unpack('!6s6s6s', self._packet[4:22])
            qos_idx = 24
            seq_idx = 22
        elif self.to_ds == 1 and self.from_ds == 0:
            (ra, ta, da) = struct.unpack('!6s6s6s', self._packet[4:22])
            qos_idx = 24
            seq_idx = 22
        elif self.to_ds == 0 and self.from_ds == 0:
            (ra, ta, bssid) = struct.unpack('!6s6s6s', self._packet[4:22])
            qos_idx = 24
            seq_idx = 22

        if ta is not None:
            ta = Wifi.get_mac_addr(ta)
        if ra is not None:
            ra = Wifi.get_mac_addr(ra)
        if sa is not None:
            sa = Wifi.get_mac_addr(sa)
        if da is not None:
            da = Wifi.get_mac_addr(da)
        if bssid is not None:
            bssid = Wifi.get_mac_addr(bssid)

        return seq_idx, qos_idx, sa, ta, ra, da, bssid
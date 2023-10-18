def strip_llc(self, idx):
        """strip(4 or 8 byte) logical link control headers
        :return: int
            number of processed bytes
        :return: dict
            llc information
        see -> http://www.wildpackets.com/resources/compendium/ethernet/frame_snap_iee8023
        ABBRVS.
        ssap: source service access point
        dsap: destination service access point
        SNAP(Subnetwork Acess Protocol)
        """
        llc = {}
        snap = 170
        llc_dsap = struct.unpack('B', self._packet[idx:idx + 1])[0]
        llc['dsap.dsap'] = llc_dsap >> 1
        llc['dsap.ig'] = llc_dsap & 0b01
        idx += 1
        llc_ssap = struct.unpack('B', self._packet[idx:idx + 1])[0]
        llc['ssap.sap'] = llc_ssap >> 1
        llc['ssap.cr'] = llc_ssap & 0b01
        idx += 1
        if llc_dsap == snap and llc_ssap == snap:
            llc_control = struct.unpack('B', self._packet[idx:idx + 1])[0]
            llc['control.u_modifier_cmd'] = llc_control >> 2
            llc['control.ftype'] = llc_control & 0x03
            idx += 1
            llc['organization_code'] = self._packet[idx:idx + 3]
            idx += 3
            llc['type'] = self._packet[idx:idx + 2]
            return 8, llc
        else:
            return 4, llc
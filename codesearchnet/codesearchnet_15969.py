def get_fixed_capabils(payload):
        """strip(2 byte) wlan_mgt.fixed.capabilities
        :payload: ctypes.structure
            2 byte
        :return: dict
            None in error
        """
        if len(payload) != 2:
            return None
        capabils = {}
        fix_cap = struct.unpack('H', payload)[0]
        cap_bits = format(fix_cap, '016b')[::-1]
        capabils['ess'] = int(cap_bits[0])             # Extended Service Set
        capabils['ibss'] = int(cap_bits[1])            # Independent Basic Service Set
        capabils['priv'] = int(cap_bits[4])            # Privacy
        capabils['short_preamble'] = int(cap_bits[5])  # Short Preamble
        capabils['pbcc'] = int(cap_bits[6])            # Packet Binary Convolutional Code
        capabils['chan_agility'] = int(cap_bits[7])    # Channel Agility
        capabils['spec_man'] = int(cap_bits[8])        # Spectrum Management
        capabils['short_slot'] = int(cap_bits[10])     # Short Slot Time
        capabils['apsd'] = int(cap_bits[11])           # Automatic Power Save Delivery
        capabils['radio_meas'] = int(cap_bits[12])     # Radio Measurement
        capabils['dss_ofdm'] = int(cap_bits[13])       # Direct Spread Spectrum
        capabils['del_back'] = int(cap_bits[14])       # Delayed Block Acknowledgement
        capabils['imm_back'] = int(cap_bits[15])       # Immediate Block Acknowledgement
        return capabils
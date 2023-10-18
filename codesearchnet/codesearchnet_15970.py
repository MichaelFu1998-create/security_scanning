def parse_vendor_ie(payload):
        """parse vendor specific information element
        oui -> organizationally unique identifier
        first 3 bytes of mac addresses
        see:https://www.wireshark.org/tools/oui-lookup.html
        strip wlan_mgt.tag.oui(3 bytes),
        wlan_mgt.tag.vendor.oui.type(1 byte)
        wlan_mgt.tag.vendor.data (varies)
        :payload: ctypes.structure
        :return: dict
            {'oui':00-11-22, 'oui_type':1, 'oui_data':ctypes.structure}
        """
        output = {}
        oui = struct.unpack('BBB', payload[0:3])
        oui = b'-'.join([('%02x' % o).encode('ascii') for o in oui])
        oui_type = struct.unpack('B', payload[3:4])[0]
        oui_data = payload[4:]
        output['oui'] = oui.upper()
        output['oui_type'] = oui_type
        output['oui_data'] = oui_data
        return output
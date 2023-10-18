def get_vendor_ies(self, mac_block=None, oui_type=None):
        """vendor information element querying
        :mac_block: str
            first 3 bytes of mac addresses in format of
            00-11-22 or 00:11:22 or 001122
        :oui_type: int
            vendors ie type
        :return: int
            is valid mac_block  format
            -1 is unknown
        :return: dict[]
            list of oui information elements
            -1 on error (invalid v
        """
        vendor_ies = []
        if mac_block is not None:
            if Management.is_valid_mac_oui(mac_block):
                mac_block = mac_block.upper()
                if ':' in mac_block:
                    mac_block.replace(':', '-')
            else:
                logging.warning("invalid oui macblock")
                return None

        for elem in self.tagged_params:
            tag_num = elem['number']
            if MNGMT_TAGS[tag_num] == 'TAG_VENDOR_SPECIFIC_IE':
                if mac_block is None:
                    vendor_ies.append(elem)
                elif elem['payload']['oui'] == mac_block.encode('ascii'):
                    if oui_type is None:
                        vendor_ies.append(elem)
                    elif elem['payload']['oui_type'] == oui_type:
                        vendor_ies.append(elem)
        return vendor_ies
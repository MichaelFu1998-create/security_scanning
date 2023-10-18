def is_valid_mac_oui(mac_block):
        """checks whether mac block is in format of
        00-11-22 or 00:11:22.
        :return: int
        """
        if len(mac_block) != 8:
            return 0
        if ':' in mac_block:
            if len(mac_block.split(':')) != 3:
                return 0
        elif '-' in mac_block:
            if len(mac_block.split('-')) != 3:
                return 0
        return 1
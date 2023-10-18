def _parse_info(self, info_field):
        """Parse the VCF info field"""
        info = dict()
        for item in info_field.split(';'):
            # Info fields may be "foo=bar" or just "foo".
            # For the first case, store key "foo" with value "bar"
            # For the second case, store key "foo" with value True.
            info_item_data = item.split('=')
            # If length is one, just store as a key with value = true.
            if len(info_item_data) == 1:
                info[info_item_data[0]] = True
            elif len(info_item_data) == 2:
                info[info_item_data[0]] = info_item_data[1]
        return info
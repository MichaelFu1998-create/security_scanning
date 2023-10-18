def __intermediate_htmode(self, radio):
        """
        only for mac80211 driver
        """
        protocol = radio.pop('protocol')
        channel_width = radio.pop('channel_width')
        # allow overriding htmode
        if 'htmode' in radio:
            return radio['htmode']
        if protocol == '802.11n':
            return 'HT{0}'.format(channel_width)
        elif protocol == '802.11ac':
            return 'VHT{0}'.format(channel_width)
        # disables n
        return 'NONE'
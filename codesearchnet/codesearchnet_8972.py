def __netjson_channel_width(self, radio):
        """
        determines NetJSON channel_width radio attribute
        """
        htmode = radio.pop('htmode')
        if htmode == 'NONE':
            return 20
        channel_width = htmode.replace('VHT', '').replace('HT', '')
        # we need to override htmode
        if '+' in channel_width or '-' in channel_width:
            radio['htmode'] = htmode
            channel_width = channel_width[0:-1]
        return int(channel_width)
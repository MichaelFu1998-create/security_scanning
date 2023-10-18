def __netjson_protocol(self, radio):
        """
        determines NetJSON protocol radio attribute
        """
        htmode = radio.get('htmode')
        hwmode = radio.get('hwmode', None)
        if htmode.startswith('HT'):
            return '802.11n'
        elif htmode.startswith('VHT'):
            return '802.11ac'
        return '802.{0}'.format(hwmode)
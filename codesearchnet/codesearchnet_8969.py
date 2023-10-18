def __intermediate_hwmode(self, radio):
        """
        possible return values are: 11a, 11b, 11g
        """
        protocol = radio['protocol']
        if protocol in ['802.11a', '802.11b', '802.11g']:
            # return 11a, 11b or 11g
            return protocol[4:]
        # determine hwmode depending on channel used
        if radio['channel'] is 0:
            # when using automatic channel selection, we need an
            # additional parameter to determine the frequency band
            return radio.get('hwmode')
        elif radio['channel'] <= 13:
            return '11g'
        else:
            return '11a'
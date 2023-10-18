def extract_protocol(self):
        """extract 802.11 protocol from radiotap.channel.flags
        :return: str
            protocol name
            one of below in success
            [.11a, .11b, .11g, .11n, .11ac]
            None in fail
        """
        if self.present.mcs:
            return '.11n'

        if self.present.vht:
            return '.11ac'

        if self.present.channel and hasattr(self, 'chan'):
            if self.chan.five_g:
                if self.chan.ofdm:
                    return '.11a'
            elif self.chan.two_g:
                if self.chan.cck:
                    return '.11b'
                elif self.chan.ofdm or self.chan.dynamic:
                    return '.11g'
        return 'None'
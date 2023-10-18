def as_tuple(self):
        """
        ping statistics.

        Returns:
            |namedtuple|:

        Examples:
            >>> import pingparsing
            >>> parser = pingparsing.PingParsing()
            >>> parser.parse(ping_result)
            >>> parser.as_tuple()
            PingResult(destination='google.com', packet_transmit=60, packet_receive=60, packet_loss_rate=0.0, packet_loss_count=0, rtt_min=61.425, rtt_avg=99.731, rtt_max=212.597, rtt_mdev=27.566, packet_duplicate_rate=0.0, packet_duplicate_count=0)
        """

        from collections import namedtuple

        ping_result = self.as_dict()

        return namedtuple("PingStatsTuple", ping_result.keys())(**ping_result)
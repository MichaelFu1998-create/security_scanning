def _fletcher16_checksum(self, data):
        """
        Calculates a fletcher16 checksum for the list of bytes
        :param data: a list of bytes that comprise the message
        :return:
        """
        sum1 = 0
        sum2 = 0

        for i, b in enumerate(data):
            sum1 += b
            sum1 &= 0xff  # Results wrapped at 16 bits
            sum2 += sum1
            sum2 &= 0xff

        logger.debug('sum1: {} sum2: {}'.format(sum1, sum2))

        return sum1, sum2
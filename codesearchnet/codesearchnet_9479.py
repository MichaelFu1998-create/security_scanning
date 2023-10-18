async def parse_line(self):
        """
        :py:func:`asyncio.coroutine`

        Parsing server response line.

        :return: (code, line)
        :rtype: (:py:class:`aioftp.Code`, :py:class:`str`)

        :raises ConnectionResetError: if received data is empty (this
            means, that connection is closed)
        :raises asyncio.TimeoutError: if there where no data for `timeout`
            period
        """
        line = await self.stream.readline()
        if not line:
            self.stream.close()
            raise ConnectionResetError
        s = line.decode(encoding=self.encoding).rstrip()
        logger.info(s)
        return Code(s[:3]), s[3:]
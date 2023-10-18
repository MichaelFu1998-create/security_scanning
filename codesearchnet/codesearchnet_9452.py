async def parse_command(self, stream):
        """
        :py:func:`asyncio.coroutine`

        Complex method for getting command.

        :param stream: connection steram
        :type stream: :py:class:`asyncio.StreamIO`

        :return: (code, rest)
        :rtype: (:py:class:`str`, :py:class:`str`)
        """
        line = await stream.readline()
        if not line:
            raise ConnectionResetError
        s = line.decode(encoding=self.encoding).rstrip()
        logger.info(s)
        cmd, _, rest = s.partition(" ")
        return cmd.lower(), rest
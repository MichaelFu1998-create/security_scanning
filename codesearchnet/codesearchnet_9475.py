async def readline(self):
        """
        :py:func:`asyncio.coroutine`

        :py:meth:`aioftp.StreamIO.readline` proxy
        """
        await self.wait("read")
        start = _now()
        data = await super().readline()
        self.append("read", data, start)
        return data
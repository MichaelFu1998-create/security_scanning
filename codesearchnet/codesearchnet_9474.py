async def read(self, count=-1):
        """
        :py:func:`asyncio.coroutine`

        :py:meth:`aioftp.StreamIO.read` proxy
        """
        await self.wait("read")
        start = _now()
        data = await super().read(count)
        self.append("read", data, start)
        return data
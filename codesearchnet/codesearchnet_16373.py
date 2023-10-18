async def byte_order(self):
        """Get the byte order used when communicating
            (should only ever be little endian using this library).
        """
        return await asyncio.wait_for(
            self._protocol.send_command("byteorder"), timeout=self._timeout
        )
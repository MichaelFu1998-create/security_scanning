async def qtm_version(self):
        """Get the QTM version.
        """
        return await asyncio.wait_for(
            self._protocol.send_command("qtmversion"), timeout=self._timeout
        )
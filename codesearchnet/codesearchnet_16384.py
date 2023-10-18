async def save(self, filename, overwrite=False):
        """Save a measurement.

        :param filename: Filename you wish to save as.
        :param overwrite: If QTM should overwrite existing measurement.
        """
        cmd = "save %s%s" % (filename, " overwrite" if overwrite else "")
        return await asyncio.wait_for(
            self._protocol.send_command(cmd), timeout=self._timeout
        )
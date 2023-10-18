async def load(self, filename):
        """Load a measurement.

        :param filename: Path to measurement you want to load.
        """
        cmd = "load %s" % filename
        return await asyncio.wait_for(
            self._protocol.send_command(cmd), timeout=self._timeout
        )
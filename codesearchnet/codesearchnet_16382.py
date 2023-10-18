async def start(self, rtfromfile=False):
        """Start RT from file. You need to be in control of QTM to be able to do this.
        """
        cmd = "start" + (" rtfromfile" if rtfromfile else "")
        return await asyncio.wait_for(
            self._protocol.send_command(cmd), timeout=self._timeout
        )
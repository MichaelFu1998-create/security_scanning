async def release_control(self):
        """Release control of QTM.
        """

        cmd = "releasecontrol"
        return await asyncio.wait_for(
            self._protocol.send_command(cmd), timeout=self._timeout
        )
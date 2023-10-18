async def set_qtm_event(self, event=None):
        """Set event in QTM."""
        cmd = "event%s" % ("" if event is None else " " + event)
        return await asyncio.wait_for(
            self._protocol.send_command(cmd), timeout=self._timeout
        )
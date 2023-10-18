async def get_state(self):
        """Get the latest state change of QTM. If the :func:`~qtm.connect` on_event
        callback was set the callback will be called as well.

        :rtype: A :class:`qtm.QRTEvent`
        """
        await self._protocol.send_command("getstate", callback=False)
        return await self._protocol.await_event()
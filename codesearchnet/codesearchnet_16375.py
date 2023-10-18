async def await_event(self, event=None, timeout=30):
        """Wait for an event from QTM.

        :param event: A :class:`qtm.QRTEvent`
            to wait for a specific event. Otherwise wait for any event.

        :param timeout: Max time to wait for event.

        :rtype: A :class:`qtm.QRTEvent`
        """
        return await self._protocol.await_event(event, timeout=timeout)
async def send_upstream(self, message, stream_name=None):
        """
        Send a message upstream to a de-multiplexed application.

        If stream_name is includes will send just to that upstream steam, if not included will send ot all upstream
        steams.
        """
        if stream_name is None:
            for steam_queue in self.application_streams.values():
                await steam_queue.put(message)
            return
        steam_queue = self.application_streams.get(stream_name)
        if steam_queue is None:
            raise ValueError("Invalid multiplexed frame received (stream not mapped)")
        await steam_queue.put(message)
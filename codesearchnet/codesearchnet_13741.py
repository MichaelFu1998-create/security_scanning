async def websocket_accept(self, message, stream_name):
        """
        Intercept downstream `websocket.accept` message and thus allow this upsteam application to accept websocket
        frames.
        """
        is_first = not self.applications_accepting_frames
        self.applications_accepting_frames.add(stream_name)
        # accept the connection after the first upstream application accepts.
        if is_first:
            await self.accept()
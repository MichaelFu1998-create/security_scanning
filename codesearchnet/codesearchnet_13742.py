async def websocket_close(self, message, stream_name):
        """
        Handle downstream `websocket.close` message.

        Will disconnect this upstream application from receiving any new frames.

        If there are not more upstream applications accepting messages it will then call `close`.
        """
        if stream_name in self.applications_accepting_frames:
            # remove from set of upsteams steams than can receive new messages
            self.applications_accepting_frames.remove(stream_name)

        # we are already closing due to an upstream websocket.disconnect command

        if self.closing:
            return
        # if none of the upstream applications are listing we need to close.
        if not self.applications_accepting_frames:
            await self.close(message.get("code"))
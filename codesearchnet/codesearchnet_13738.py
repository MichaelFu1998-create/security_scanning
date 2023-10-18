async def websocket_disconnect(self, message):
        """
        Handle the disconnect message.

        This is propagated to all upstream applications.
        """
        # set this flag so as to ensure we don't send a downstream `websocket.close` message due to all
        # child applications closing.
        self.closing = True
        # inform all children
        await self.send_upstream(message)
        await super().websocket_disconnect(message)
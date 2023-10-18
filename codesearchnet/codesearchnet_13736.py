async def dispatch_downstream(self, message, steam_name):
        """
        Handle a downstream message coming from an upstream steam.

        if there is not handling method set for this method type it will propagate the message further downstream.

        This is called as part of the co-routine of an upstream steam, not the same loop as used for upstream messages
        in the de-multiplexer.
        """
        handler = getattr(self, get_handler_name(message), None)
        if handler:
            await handler(message, stream_name=steam_name)
        else:
            # if there is not handler then just pass the message further downstream.
            await self.base_send(message)
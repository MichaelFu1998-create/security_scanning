async def _on_event(self, event_):
        """Receive a hangouts_pb2.Event and fan out to Conversations.

        Args:
            event_: hangouts_pb2.Event instance
        """
        conv_id = event_.conversation_id.id
        try:
            conv = await self._get_or_fetch_conversation(conv_id)
        except exceptions.NetworkError:
            logger.warning(
                'Failed to fetch conversation for event notification: %s',
                conv_id
            )
        else:
            self._sync_timestamp = parsers.from_timestamp(event_.timestamp)
            conv_event = conv.add_event(event_)
            # conv_event may be None if the event was a duplicate.
            if conv_event is not None:
                await self.on_event.fire(conv_event)
                await conv.on_event.fire(conv_event)
async def _on_state_update(self, state_update):
        """Receive a StateUpdate and fan out to Conversations.

        Args:
            state_update: hangouts_pb2.StateUpdate instance
        """
        # The state update will include some type of notification:
        notification_type = state_update.WhichOneof('state_update')

        # If conversation fields have been updated, the state update will have
        # a conversation containing changed fields. Handle updating the
        # conversation from this delta:
        if state_update.HasField('conversation'):
            try:
                await self._handle_conversation_delta(
                    state_update.conversation
                )
            except exceptions.NetworkError:
                logger.warning(
                    'Discarding %s for %s: Failed to fetch conversation',
                    notification_type.replace('_', ' '),
                    state_update.conversation.conversation_id.id
                )
                return

        if notification_type == 'typing_notification':
            await self._handle_set_typing_notification(
                state_update.typing_notification
            )
        elif notification_type == 'watermark_notification':
            await self._handle_watermark_notification(
                state_update.watermark_notification
            )
        elif notification_type == 'event_notification':
            await self._on_event(
                state_update.event_notification.event
            )
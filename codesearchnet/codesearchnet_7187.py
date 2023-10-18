async def _handle_conversation_delta(self, conversation):
        """Receive Conversation delta and create or update the conversation.

        Args:
            conversation: hangouts_pb2.Conversation instance

        Raises:
            NetworkError: A request to fetch the complete conversation failed.
        """
        conv_id = conversation.conversation_id.id
        conv = self._conv_dict.get(conv_id, None)
        if conv is None:
            # Ignore the delta and fetch the complete conversation.
            await self._get_or_fetch_conversation(conv_id)
        else:
            # Update conversation using the delta.
            conv.update_conversation(conversation)
async def rename(self, name):
        """Rename this conversation.

        Hangouts only officially supports renaming group conversations, so
        custom names for one-to-one conversations may or may not appear in all
        first party clients.

        Args:
            name (str): New name.

        Raises:
            .NetworkError: If conversation cannot be renamed.
        """
        await self._client.rename_conversation(
            hangouts_pb2.RenameConversationRequest(
                request_header=self._client.get_request_header(),
                new_name=name,
                event_request_header=self._get_event_request_header(),
            )
        )
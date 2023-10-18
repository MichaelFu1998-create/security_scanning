async def delete_conversation(self, delete_conversation_request):
        """Leave a one-to-one conversation.

        One-to-one conversations are "sticky"; they can't actually be deleted.
        This API clears the event history of the specified conversation up to
        ``delete_upper_bound_timestamp``, hiding it if no events remain.
        """
        response = hangouts_pb2.DeleteConversationResponse()
        await self._pb_request('conversations/deleteconversation',
                               delete_conversation_request, response)
        return response
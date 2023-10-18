async def get_conversation(self, get_conversation_request):
        """Return conversation info and recent events."""
        response = hangouts_pb2.GetConversationResponse()
        await self._pb_request('conversations/getconversation',
                               get_conversation_request, response)
        return response
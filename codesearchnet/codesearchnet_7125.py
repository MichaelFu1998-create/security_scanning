async def create_conversation(self, create_conversation_request):
        """Create a new conversation."""
        response = hangouts_pb2.CreateConversationResponse()
        await self._pb_request('conversations/createconversation',
                               create_conversation_request, response)
        return response
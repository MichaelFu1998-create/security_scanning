async def send_chat_message(self, send_chat_message_request):
        """Send a chat message to a conversation."""
        response = hangouts_pb2.SendChatMessageResponse()
        await self._pb_request('conversations/sendchatmessage',
                               send_chat_message_request, response)
        return response
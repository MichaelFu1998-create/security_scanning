async def set_typing(self, set_typing_request):
        """Set the typing status of a conversation."""
        response = hangouts_pb2.SetTypingResponse()
        await self._pb_request('conversations/settyping',
                               set_typing_request, response)
        return response
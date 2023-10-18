async def modify_otr_status(self, modify_otr_status_request):
        """Enable or disable message history in a conversation."""
        response = hangouts_pb2.ModifyOTRStatusResponse()
        await self._pb_request('conversations/modifyotrstatus',
                               modify_otr_status_request, response)
        return response
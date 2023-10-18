async def get_group_conversation_url(self,
                                         get_group_conversation_url_request):
        """Get URL to allow others to join a group conversation."""
        response = hangouts_pb2.GetGroupConversationUrlResponse()
        await self._pb_request('conversations/getgroupconversationurl',
                               get_group_conversation_url_request,
                               response)
        return response
async def sync_recent_conversations(
            self, sync_recent_conversations_request
    ):
        """Return info on recent conversations and their events."""
        response = hangouts_pb2.SyncRecentConversationsResponse()
        await self._pb_request('conversations/syncrecentconversations',
                               sync_recent_conversations_request,
                               response)
        return response
async def query_presence(self, query_presence_request):
        """Return presence status for a list of users."""
        response = hangouts_pb2.QueryPresenceResponse()
        await self._pb_request('presence/querypresence',
                               query_presence_request, response)
        return response
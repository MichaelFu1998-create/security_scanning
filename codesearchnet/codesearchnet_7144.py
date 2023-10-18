async def set_presence(self, set_presence_request):
        """Set the presence status."""
        response = hangouts_pb2.SetPresenceResponse()
        await self._pb_request('presence/setpresence',
                               set_presence_request, response)
        return response
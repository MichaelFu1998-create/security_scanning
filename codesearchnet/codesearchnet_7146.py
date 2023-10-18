async def sync_all_new_events(self, sync_all_new_events_request):
        """List all events occurring at or after a timestamp."""
        response = hangouts_pb2.SyncAllNewEventsResponse()
        await self._pb_request('conversations/syncallnewevents',
                               sync_all_new_events_request, response)
        return response
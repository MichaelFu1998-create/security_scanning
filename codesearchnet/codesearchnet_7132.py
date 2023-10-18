async def get_suggested_entities(self, get_suggested_entities_request):
        """Return suggested contacts."""
        response = hangouts_pb2.GetSuggestedEntitiesResponse()
        await self._pb_request('contacts/getsuggestedentities',
                               get_suggested_entities_request, response)
        return response
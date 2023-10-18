async def search_entities(self, search_entities_request):
        """Return user entities based on a query."""
        response = hangouts_pb2.SearchEntitiesResponse()
        await self._pb_request('contacts/searchentities',
                               search_entities_request, response)
        return response
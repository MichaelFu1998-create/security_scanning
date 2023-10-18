async def easter_egg(self, easter_egg_request):
        """Send an easter egg event to a conversation."""
        response = hangouts_pb2.EasterEggResponse()
        await self._pb_request('conversations/easteregg',
                               easter_egg_request, response)
        return response
async def set_active_client(self, set_active_client_request):
        """Set the active client."""
        response = hangouts_pb2.SetActiveClientResponse()
        await self._pb_request('clients/setactiveclient',
                               set_active_client_request, response)
        return response
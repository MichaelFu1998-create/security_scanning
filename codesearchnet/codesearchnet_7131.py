async def get_self_info(self, get_self_info_request):
        """Return info about the current user."""
        response = hangouts_pb2.GetSelfInfoResponse()
        await self._pb_request('contacts/getselfinfo',
                               get_self_info_request, response)
        return response
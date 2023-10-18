async def add_user(self, add_user_request):
        """Invite users to join an existing group conversation."""
        response = hangouts_pb2.AddUserResponse()
        await self._pb_request('conversations/adduser',
                               add_user_request, response)
        return response
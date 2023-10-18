async def remove_user(self, remove_user_request):
        """Remove a participant from a group conversation."""
        response = hangouts_pb2.RemoveUserResponse()
        await self._pb_request('conversations/removeuser',
                               remove_user_request, response)
        return response
async def set_focus(self, set_focus_request):
        """Set focus to a conversation."""
        response = hangouts_pb2.SetFocusResponse()
        await self._pb_request('conversations/setfocus',
                               set_focus_request, response)
        return response
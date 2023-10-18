async def set_group_link_sharing_enabled(
            self, set_group_link_sharing_enabled_request
    ):
        """Set whether group link sharing is enabled for a conversation."""
        response = hangouts_pb2.SetGroupLinkSharingEnabledResponse()
        await self._pb_request('conversations/setgrouplinksharingenabled',
                               set_group_link_sharing_enabled_request,
                               response)
        return response
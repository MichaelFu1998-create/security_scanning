async def send_offnetwork_invitation(
            self, send_offnetwork_invitation_request
    ):
        """Send an email to invite a non-Google contact to Hangouts."""
        response = hangouts_pb2.SendOffnetworkInvitationResponse()
        await self._pb_request('devices/sendoffnetworkinvitation',
                               send_offnetwork_invitation_request,
                               response)
        return response
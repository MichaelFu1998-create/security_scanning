async def update_watermark(self, update_watermark_request):
        """Update the watermark (read timestamp) of a conversation."""
        response = hangouts_pb2.UpdateWatermarkResponse()
        await self._pb_request('conversations/updatewatermark',
                               update_watermark_request, response)
        return response
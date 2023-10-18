async def _handle_watermark_notification(self, watermark_notification):
        """Receive WatermarkNotification and update the conversation.

        Args:
            watermark_notification: hangouts_pb2.WatermarkNotification instance
        """
        conv_id = watermark_notification.conversation_id.id
        res = parsers.parse_watermark_notification(watermark_notification)
        await self.on_watermark_notification.fire(res)
        try:
            conv = await self._get_or_fetch_conversation(conv_id)
        except exceptions.NetworkError:
            logger.warning(
                'Failed to fetch conversation for watermark notification: %s',
                conv_id
            )
        else:
            await conv.on_watermark_notification.fire(res)
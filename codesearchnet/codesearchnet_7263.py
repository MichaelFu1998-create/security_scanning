def attachments(self):
        """List of attachments in the message (:class:`list`)."""
        raw_attachments = self._event.chat_message.message_content.attachment
        if raw_attachments is None:
            raw_attachments = []
        attachments = []
        for attachment in raw_attachments:
            for embed_item_type in attachment.embed_item.type:
                known_types = [
                    hangouts_pb2.ITEM_TYPE_PLUS_PHOTO,
                    hangouts_pb2.ITEM_TYPE_PLACE_V2,
                    hangouts_pb2.ITEM_TYPE_PLACE,
                    hangouts_pb2.ITEM_TYPE_THING,
                ]
                if embed_item_type not in known_types:
                    logger.warning('Received chat message attachment with '
                                   'unknown embed type: %r', embed_item_type)

            if attachment.embed_item.HasField('plus_photo'):
                attachments.append(
                    attachment.embed_item.plus_photo.thumbnail.image_url
                )
        return attachments
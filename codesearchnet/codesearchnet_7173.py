async def send_message(self, segments, image_file=None, image_id=None,
                           image_user_id=None):
        """Send a message to this conversation.

        A per-conversation lock is acquired to ensure that messages are sent in
        the correct order when this method is called multiple times
        asynchronously.

        Args:
            segments: List of :class:`.ChatMessageSegment` objects to include
                in the message.
            image_file: (optional) File-like object containing an image to be
                attached to the message.
            image_id: (optional) ID of an Picasa photo to be attached to the
                message. If you specify both ``image_file`` and ``image_id``
                together, ``image_file`` takes precedence and ``image_id`` will
                be ignored.
            image_user_id: (optional) Picasa user ID, required only if
                ``image_id`` refers to an image from a different Picasa user,
                such as Google's sticker user.

        Raises:
            .NetworkError: If the message cannot be sent.
        """
        async with self._send_message_lock:
            if image_file:
                try:
                    uploaded_image = await self._client.upload_image(
                        image_file, return_uploaded_image=True
                    )
                except exceptions.NetworkError as e:
                    logger.warning('Failed to upload image: {}'.format(e))
                    raise
                image_id = uploaded_image.image_id
            try:
                request = hangouts_pb2.SendChatMessageRequest(
                    request_header=self._client.get_request_header(),
                    event_request_header=self._get_event_request_header(),
                    message_content=hangouts_pb2.MessageContent(
                        segment=[seg.serialize() for seg in segments],
                    ),
                )
                if image_id is not None:
                    request.existing_media.photo.photo_id = image_id
                if image_user_id is not None:
                    request.existing_media.photo.user_id = image_user_id
                    request.existing_media.photo.is_custom_user_id = True
                await self._client.send_chat_message(request)
            except exceptions.NetworkError as e:
                logger.warning('Failed to send message: {}'.format(e))
                raise
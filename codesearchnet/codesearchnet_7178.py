async def update_read_timestamp(self, read_timestamp=None):
        """Update the timestamp of the latest event which has been read.

        This method will avoid making an API request if it will have no effect.

        Args:
            read_timestamp (datetime.datetime): (optional) Timestamp to set.
                Defaults to the timestamp of the newest event.

        Raises:
            .NetworkError: If the timestamp cannot be updated.
        """
        if read_timestamp is None:
            read_timestamp = (self.events[-1].timestamp if self.events else
                              datetime.datetime.now(datetime.timezone.utc))
        if read_timestamp > self.latest_read_timestamp:
            logger.info(
                'Setting {} latest_read_timestamp from {} to {}'
                .format(self.id_, self.latest_read_timestamp, read_timestamp)
            )
            # Prevent duplicate requests by updating the conversation now.
            state = self._conversation.self_conversation_state
            state.self_read_state.latest_read_timestamp = (
                parsers.to_timestamp(read_timestamp)
            )
            try:
                await self._client.update_watermark(
                    hangouts_pb2.UpdateWatermarkRequest(
                        request_header=self._client.get_request_header(),
                        conversation_id=hangouts_pb2.ConversationId(
                            id=self.id_
                        ),
                        last_read_timestamp=parsers.to_timestamp(
                            read_timestamp
                        ),
                    )
                )
            except exceptions.NetworkError as e:
                logger.warning('Failed to update read timestamp: {}'.format(e))
                raise
async def _sync(self):
        """Sync conversation state and events that could have been missed."""
        logger.info('Syncing events since {}'.format(self._sync_timestamp))
        try:
            res = await self._client.sync_all_new_events(
                hangouts_pb2.SyncAllNewEventsRequest(
                    request_header=self._client.get_request_header(),
                    last_sync_timestamp=parsers.to_timestamp(
                        self._sync_timestamp
                    ),
                    max_response_size_bytes=1048576,  # 1 MB
                )
            )
        except exceptions.NetworkError as e:
            logger.warning('Failed to sync events, some events may be lost: {}'
                           .format(e))
        else:
            for conv_state in res.conversation_state:
                conv_id = conv_state.conversation_id.id
                conv = self._conv_dict.get(conv_id, None)
                if conv is not None:
                    conv.update_conversation(conv_state.conversation)
                    for event_ in conv_state.event:
                        timestamp = parsers.from_timestamp(event_.timestamp)
                        if timestamp > self._sync_timestamp:
                            # This updates the sync_timestamp for us, as well
                            # as triggering events.
                            await self._on_event(event_)
                else:
                    self._add_conversation(
                        conv_state.conversation,
                        conv_state.event,
                        conv_state.event_continuation_token
                    )
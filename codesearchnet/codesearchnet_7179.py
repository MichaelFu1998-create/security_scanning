async def get_events(self, event_id=None, max_events=50):
        """Get events from this conversation.

        Makes a request to load historical events if necessary.

        Args:
            event_id (str): (optional) If provided, return events preceding
                this event, otherwise return the newest events.
            max_events (int): Maximum number of events to return. Defaults to
                50.

        Returns:
            List of :class:`.ConversationEvent` instances, ordered
            newest-first.

        Raises:
            KeyError: If ``event_id`` does not correspond to a known event.
            .NetworkError: If the events could not be requested.
        """
        if event_id is None:
            # If no event_id is provided, return the newest events in this
            # conversation.
            conv_events = self._events[-1 * max_events:]
        else:
            # If event_id is provided, return the events we have that are
            # older, or request older events if event_id corresponds to the
            # oldest event we have.
            conv_event = self.get_event(event_id)
            if self._events[0].id_ != event_id:
                conv_events = self._events[self._events.index(conv_event) + 1:]
            else:
                logger.info('Loading events for conversation {} before {}'
                            .format(self.id_, conv_event.timestamp))
                res = await self._client.get_conversation(
                    hangouts_pb2.GetConversationRequest(
                        request_header=self._client.get_request_header(),
                        conversation_spec=hangouts_pb2.ConversationSpec(
                            conversation_id=hangouts_pb2.ConversationId(
                                id=self.id_
                            )
                        ),
                        include_event=True,
                        max_events_per_conversation=max_events,
                        event_continuation_token=self._event_cont_token
                    )
                )
                # Certain fields of conversation_state are not populated by
                # SyncRecentConversations. This is the case with the
                # user_read_state fields which are all set to 0 but for the
                # 'self' user. Update here so these fields get populated on the
                # first call to GetConversation.
                if res.conversation_state.HasField('conversation'):
                    self.update_conversation(
                        res.conversation_state.conversation
                    )
                self._event_cont_token = (
                    res.conversation_state.event_continuation_token
                )
                conv_events = [self._wrap_event(event) for event
                               in res.conversation_state.event]
                logger.info('Loaded {} events for conversation {}'
                            .format(len(conv_events), self.id_))
                # Iterate though the events newest to oldest.
                for conv_event in reversed(conv_events):
                    # Add event as the new oldest event, unless we already have
                    # it.
                    if conv_event.id_ not in self._events_dict:
                        self._events.insert(0, conv_event)
                        self._events_dict[conv_event.id_] = conv_event
                    else:
                        # If this happens, there's probably a bug.
                        logger.info(
                            'Conversation %s ignoring duplicate event %s',
                            self.id_, conv_event.id_
                        )
        return conv_events
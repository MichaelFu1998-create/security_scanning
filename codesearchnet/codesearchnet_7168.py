def update_conversation(self, conversation):
        """Update the internal state of the conversation.

        This method is used by :class:`.ConversationList` to maintain this
        instance.

        Args:
            conversation: ``Conversation`` message.
        """
        # StateUpdate.conversation is actually a delta; fields that aren't
        # specified are assumed to be unchanged. Until this class is
        # refactored, hide this by saving and restoring previous values where
        # necessary.

        new_state = conversation.self_conversation_state
        old_state = self._conversation.self_conversation_state
        self._conversation = conversation

        # delivery_medium_option
        if not new_state.delivery_medium_option:
            new_state.delivery_medium_option.extend(
                old_state.delivery_medium_option
            )

        # latest_read_timestamp
        old_timestamp = old_state.self_read_state.latest_read_timestamp
        new_timestamp = new_state.self_read_state.latest_read_timestamp
        if new_timestamp == 0:
            new_state.self_read_state.latest_read_timestamp = old_timestamp

        # user_read_state(s)
        for new_entry in conversation.read_state:
            tstamp = parsers.from_timestamp(new_entry.latest_read_timestamp)
            if tstamp == 0:
                continue
            uid = parsers.from_participantid(new_entry.participant_id)
            if uid not in self._watermarks or self._watermarks[uid] < tstamp:
                self._watermarks[uid] = tstamp
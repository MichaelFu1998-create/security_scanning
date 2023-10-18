def add_event(self, event_):
        """Add an event to the conversation.

        This method is used by :class:`.ConversationList` to maintain this
        instance.

        Args:
            event_: ``Event`` message.

        Returns:
            :class:`.ConversationEvent` representing the event.
        """
        conv_event = self._wrap_event(event_)
        if conv_event.id_ not in self._events_dict:
            self._events.append(conv_event)
            self._events_dict[conv_event.id_] = conv_event
        else:
            # If this happens, there's probably a bug.
            logger.info('Conversation %s ignoring duplicate event %s',
                        self.id_, conv_event.id_)
            return None
        return conv_event
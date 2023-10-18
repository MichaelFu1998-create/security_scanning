def _ignore_event(self, message):
        """
        message_replied event is not truly a message event and does not have a message.text
        don't process such events

        commands may not be idempotent, so ignore message_changed events.
        """
        if hasattr(message, 'subtype') and message.subtype in self.ignored_events:
            return True
        return False
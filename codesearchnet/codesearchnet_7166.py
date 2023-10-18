def is_quiet(self):
        """``True`` if notification level for this conversation is quiet."""
        level = self._conversation.self_conversation_state.notification_level
        return level == hangouts_pb2.NOTIFICATION_LEVEL_QUIET
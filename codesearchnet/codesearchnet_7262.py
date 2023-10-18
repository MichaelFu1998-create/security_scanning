def segments(self):
        """List of :class:`ChatMessageSegment` in message (:class:`list`)."""
        seg_list = self._event.chat_message.message_content.segment
        return [ChatMessageSegment.deserialize(seg) for seg in seg_list]
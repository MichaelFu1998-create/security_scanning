def deserialize(segment):
        """Construct :class:`ChatMessageSegment` from ``Segment`` message.

        Args:
            segment: ``Segment`` message to parse.

        Returns:
            :class:`ChatMessageSegment` object.
        """
        link_target = segment.link_data.link_target
        return ChatMessageSegment(
            segment.text, segment_type=segment.type,
            is_bold=segment.formatting.bold,
            is_italic=segment.formatting.italic,
            is_strikethrough=segment.formatting.strikethrough,
            is_underline=segment.formatting.underline,
            link_target=None if link_target == '' else link_target
        )
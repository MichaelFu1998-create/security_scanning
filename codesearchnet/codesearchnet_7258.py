def from_str(text):
        """Construct :class:`ChatMessageSegment` list parsed from a string.

        Args:
            text (str): Text to parse. May contain line breaks, URLs and
                formatting markup (simplified Markdown and HTML) to be
                converted into equivalent segments.

        Returns:
            List of :class:`ChatMessageSegment` objects.
        """
        segment_list = chat_message_parser.parse(text)
        return [ChatMessageSegment(segment.text, **segment.params)
                for segment in segment_list]
def serialize(self):
        """Serialize this segment to a ``Segment`` message.

        Returns:
            ``Segment`` message.
        """
        segment = hangouts_pb2.Segment(
            type=self.type_,
            text=self.text,
            formatting=hangouts_pb2.Formatting(
                bold=self.is_bold,
                italic=self.is_italic,
                strikethrough=self.is_strikethrough,
                underline=self.is_underline,
            ),
        )
        if self.link_target is not None:
            segment.link_data.link_target = self.link_target
        return segment
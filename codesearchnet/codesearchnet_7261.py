def text(self):
        """Text of the message without formatting (:class:`str`)."""
        lines = ['']
        for segment in self.segments:
            if segment.type_ == hangouts_pb2.SEGMENT_TYPE_TEXT:
                lines[-1] += segment.text
            elif segment.type_ == hangouts_pb2.SEGMENT_TYPE_LINK:
                lines[-1] += segment.text
            elif segment.type_ == hangouts_pb2.SEGMENT_TYPE_LINE_BREAK:
                lines.append('')
            else:
                logger.warning('Ignoring unknown chat message segment type: {}'
                               .format(segment.type_))
        lines.extend(self.attachments)
        return '\n'.join(lines)
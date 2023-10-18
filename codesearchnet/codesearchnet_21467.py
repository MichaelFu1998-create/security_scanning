def write(self, writer):
        """
        Writes an XML representation of this node (including descendants) to the specified file-like object.

        :param writer: An :class:`XmlWriter` instance to write this node to
        """
        multiline = bool(self._children)
        newline_start = multiline and not bool(self.data)
        writer.start(self.tagname, self.attrs, newline=newline_start)
        if self.data:
            writer.data(self.data, newline=bool(self._children))
        for c in self._children:
            c.write(writer)
        writer.end(self.tagname, indent=multiline)
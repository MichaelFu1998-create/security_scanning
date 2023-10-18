def xml(self, **kwargs):
        """
        Returns an XML representation of this node (including descendants). This method automatically creates an
        :class:`XmlWriter` instance internally to handle the writing.

        :param **kwargs: Any named arguments are passed along to the :class:`XmlWriter` constructor
        """
        s = bytes_io()
        writer = XmlWriter(s, **kwargs)
        self.write(writer)
        return s.getvalue()
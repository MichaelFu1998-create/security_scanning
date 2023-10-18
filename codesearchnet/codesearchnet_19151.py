def _readxml(self):
        """Read a block and return the result as XML

        :return: block as xml
        :rtype: xml.etree.ElementTree

        """
        block = re.sub(r'<(/?)s>', r'&lt;\1s&gt;', self._readblock())
        try:
            xml = XML(block)
        except ParseError:
            xml = None
        return xml
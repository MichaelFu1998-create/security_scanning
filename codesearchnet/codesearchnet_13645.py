def _from_xml(self, element):
        """Initialize an ErrorElement object from an XML element.

        :Parameters:
            - `element`: XML element to be decoded.
        :Types:
            - `element`: :etree:`ElementTree.Element`
        """
        ErrorElement._from_xml(self, element)
        error_type = element.get(u"type")
        if error_type:
            self.error_type = error_type
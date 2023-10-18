def as_xml(self, stanza_namespace = None): # pylint: disable-msg=W0221
        """Return the XML error representation.

        :Parameters:
            - `stanza_namespace`: namespace URI of the containing stanza
        :Types:
            - `stanza_namespace`: `unicode`

        :returntype: :etree:`ElementTree.Element`"""
        if stanza_namespace:
            self.error_qname = "{{{0}}}error".format(stanza_namespace)
            self.text_qname = "{{{0}}}text".format(stanza_namespace)
        result = ErrorElement.as_xml(self)
        result.set("type", self.error_type)
        return result
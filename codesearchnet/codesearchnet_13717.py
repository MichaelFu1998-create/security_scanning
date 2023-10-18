def complete_xml_element(self, xmlnode, _unused):
        """Complete the XML node with `self` content.

        Should be overriden in classes derived from `StanzaPayloadObject`.

        :Parameters:
            - `xmlnode`: XML node with the element being built. It has already
              right name and namespace, but no attributes or content.
            - `_unused`: document to which the element belongs.
        :Types:
            - `xmlnode`: `libxml2.xmlNode`
            - `_unused`: `libxml2.xmlDoc`"""
        tm=self.timestamp.strftime("%Y%m%dT%H:%M:%S")
        xmlnode.setProp("stamp",tm)
        if self.delay_from:
            xmlnode.setProp("from",self.delay_from.as_utf8())
        if self.reason:
            xmlnode.setContent(to_utf8(self.reason))
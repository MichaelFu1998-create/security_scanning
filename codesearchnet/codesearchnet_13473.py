def complete_xml_element(self, xmlnode, doc):
        """Complete the XML node with `self` content.

        :Parameters:
            - `xmlnode`: XML node with the element being built. It has already
              right name and namespace, but no attributes or content.
            - `doc`: document to which the element belongs.
        :Types:
            - `xmlnode`: `libxml2.xmlNode`
            - `doc`: `libxml2.xmlDoc`"""
        _unused = doc
        if self.label is not None:
            xmlnode.setProp("label", self.label.encode("utf-8"))
        xmlnode.newTextChild(xmlnode.ns(), "value", self.value.encode("utf-8"))
        return xmlnode
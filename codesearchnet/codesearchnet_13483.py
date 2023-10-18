def complete_xml_element(self, xmlnode, doc):
        """Complete the XML node with `self` content.

        :Parameters:
            - `xmlnode`: XML node with the element being built. It has already
              right name and namespace, but no attributes or content.
            - `doc`: document to which the element belongs.
        :Types:
            - `xmlnode`: `libxml2.xmlNode`
            - `doc`: `libxml2.xmlDoc`"""
        if self.type not in self.allowed_types:
            raise ValueError("Form type %r not allowed." % (self.type,))
        xmlnode.setProp("type", self.type)
        if self.type == "cancel":
            return
        ns = xmlnode.ns()
        if self.title is not None:
            xmlnode.newTextChild(ns, "title", to_utf8(self.title))
        if self.instructions is not None:
            xmlnode.newTextChild(ns, "instructions", to_utf8(self.instructions))
        for field in self.fields:
            field.as_xml(xmlnode, doc)
        if self.type != "result":
            return
        if self.reported_fields:
            reported = xmlnode.newChild(ns, "reported", None)
            for field in self.reported_fields:
                field.as_xml(reported, doc)
        for item in self.items:
            item.as_xml(xmlnode, doc)
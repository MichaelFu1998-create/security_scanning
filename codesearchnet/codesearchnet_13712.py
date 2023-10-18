def complete_xml_element(self, xmlnode, doc):
        """Complete the XML node with `self` content.

        :Parameters:
            - `xmlnode`: XML node with the element being built. It has already
              right name and namespace, but no attributes or content.
            - `doc`: document to which the element belongs.
        :Types:
            - `xmlnode`: `libxml2.xmlNode`
            - `doc`: `libxml2.xmlDoc`"""
        ns = xmlnode.ns()
        if self.instructions is not None:
            xmlnode.newTextChild(ns, "instructions", to_utf8(self.instructions))
        if self.form:
            self.form.as_xml(xmlnode, doc)
        if self.remove:
            xmlnode.newChild(ns, "remove", None)
        else:
            if self.registered:
                xmlnode.newChild(ns, "registered", None)
            for field in legacy_fields:
                value = getattr(self, field)
                if value is not None:
                    xmlnode.newTextChild(ns, field, to_utf8(value))
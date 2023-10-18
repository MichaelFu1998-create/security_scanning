def complete_xml_element(self, xmlnode, doc):
        """Complete the XML node with `self` content.

        :Parameters:
            - `xmlnode`: XML node with the element being built. It has already
              right name and namespace, but no attributes or content.
            - `doc`: document to which the element belongs.
        :Types:
            - `xmlnode`: `libxml2.xmlNode`
            - `doc`: `libxml2.xmlDoc`"""
        if self.type is not None and self.type not in self.allowed_types:
            raise ValueError("Invalid form field type: %r" % (self.type,))
        if self.type is not None:
            xmlnode.setProp("type", self.type)
        if not self.label is None:
            xmlnode.setProp("label", to_utf8(self.label))
        if not self.name is None:
            xmlnode.setProp("var", to_utf8(self.name))
        if self.values:
            if self.type and len(self.values) > 1 and not self.type.endswith(u"-multi"):
                raise ValueError("Multiple values not allowed for %r field" % (self.type,))
            for value in self.values:
                xmlnode.newTextChild(xmlnode.ns(), "value", to_utf8(value))
        for option in self.options:
            option.as_xml(xmlnode, doc)
        if self.required:
            xmlnode.newChild(xmlnode.ns(), "required", None)
        if self.desc:
            xmlnode.newTextChild(xmlnode.ns(), "desc", to_utf8(self.desc))
        return xmlnode
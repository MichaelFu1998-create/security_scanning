def _new_from_xml(cls, xmlnode):
        """Create a new `Option` object from an XML element.

        :Parameters:
            - `xmlnode`: the XML element.
        :Types:
            - `xmlnode`: `libxml2.xmlNode`

        :return: the object created.
        :returntype: `Option`
        """
        label = from_utf8(xmlnode.prop("label"))
        child = xmlnode.children
        value = None
        for child in xml_element_ns_iter(xmlnode.children, DATAFORM_NS):
            if child.name == "value":
                value = from_utf8(child.getContent())
                break
        if value is None:
            raise BadRequestProtocolError("No value in <option/> element")
        return cls(value, label)
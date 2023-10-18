def _new_from_xml(cls, xmlnode):
        """Create a new `Field` object from an XML element.

        :Parameters:
            - `xmlnode`: the XML element.
        :Types:
            - `xmlnode`: `libxml2.xmlNode`

        :return: the object created.
        :returntype: `Field`
        """
        field_type = xmlnode.prop("type")
        label = from_utf8(xmlnode.prop("label"))
        name = from_utf8(xmlnode.prop("var"))
        child = xmlnode.children
        values = []
        options = []
        required = False
        desc = None
        while child:
            if child.type != "element" or child.ns().content != DATAFORM_NS:
                pass
            elif child.name == "required":
                required = True
            elif child.name == "desc":
                desc = from_utf8(child.getContent())
            elif child.name == "value":
                values.append(from_utf8(child.getContent()))
            elif child.name == "option":
                options.append(Option._new_from_xml(child))
            child = child.next
        if field_type and not field_type.endswith("-multi") and len(values) > 1:
            raise BadRequestProtocolError("Multiple values for a single-value field")
        return cls(name, values, field_type, label, options, required, desc)
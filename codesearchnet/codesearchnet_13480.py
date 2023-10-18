def _new_from_xml(cls, xmlnode):
        """Create a new `Item` object from an XML element.

        :Parameters:
            - `xmlnode`: the XML element.
        :Types:
            - `xmlnode`: `libxml2.xmlNode`

        :return: the object created.
        :returntype: `Item`
        """
        child = xmlnode.children
        fields = []
        while child:
            if child.type != "element" or child.ns().content != DATAFORM_NS:
                pass
            elif child.name == "field":
                fields.append(Field._new_from_xml(child))
            child = child.next
        return cls(fields)
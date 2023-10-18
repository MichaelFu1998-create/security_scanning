def __from_xml(self, xmlnode):
        """Initialize a `Form` object from an XML element.

        :Parameters:
            - `xmlnode`: the XML element.
        :Types:
            - `xmlnode`: `libxml2.xmlNode`
        """
        self.fields = []
        self.reported_fields = []
        self.items = []
        self.title = None
        self.instructions = None
        if (xmlnode.type != "element" or xmlnode.name != "x"
                or xmlnode.ns().content != DATAFORM_NS):
            raise ValueError("Not a form: " + xmlnode.serialize())
        self.type = xmlnode.prop("type")
        if not self.type in self.allowed_types:
            raise BadRequestProtocolError("Bad form type: %r" % (self.type,))
        child = xmlnode.children
        while child:
            if child.type != "element" or child.ns().content != DATAFORM_NS:
                pass
            elif child.name == "title":
                self.title = from_utf8(child.getContent())
            elif child.name == "instructions":
                self.instructions = from_utf8(child.getContent())
            elif child.name == "field":
                self.fields.append(Field._new_from_xml(child))
            elif child.name == "item":
                self.items.append(Item._new_from_xml(child))
            elif child.name == "reported":
                self.__get_reported(child)
            child = child.next
def __from_xml(self, xmlnode):
        """Initialize `Register` from an XML node.

        :Parameters:
            - `xmlnode`: the jabber:x:register XML element.
        :Types:
            - `xmlnode`: `libxml2.xmlNode`"""

        self.__logger.debug("Converting jabber:iq:register element from XML")
        if xmlnode.type!="element":
            raise ValueError("XML node is not a jabber:iq:register element (not an element)")
        ns=get_node_ns_uri(xmlnode)
        if ns and ns!=REGISTER_NS or xmlnode.name!="query":
            raise ValueError("XML node is not a jabber:iq:register element")

        for element in xml_element_iter(xmlnode.children):
            ns = get_node_ns_uri(element)
            if ns == DATAFORM_NS and element.name == "x" and not self.form:
                self.form = Form(element)
            elif ns != REGISTER_NS:
                continue
            name = element.name
            if name == "instructions" and not self.instructions:
                self.instructions = from_utf8(element.getContent())
            elif name == "registered":
                self.registered = True
            elif name == "remove":
                self.remove = True
            elif name in legacy_fields and not getattr(self, name):
                value = from_utf8(element.getContent())
                if value is None:
                    value = u""
                self.__logger.debug(u"Setting legacy field %r to %r" % (name, value))
                setattr(self, name, value)
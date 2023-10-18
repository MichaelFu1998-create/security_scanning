def __get_reported(self, xmlnode):
        """Parse the <reported/> element of the form.

        :Parameters:
            - `xmlnode`: the element to parse.
        :Types:
            - `xmlnode`: `libxml2.xmlNode`"""
        child = xmlnode.children
        while child:
            if child.type != "element" or child.ns().content != DATAFORM_NS:
                pass
            elif child.name == "field":
                self.reported_fields.append(Field._new_from_xml(child))
            child = child.next
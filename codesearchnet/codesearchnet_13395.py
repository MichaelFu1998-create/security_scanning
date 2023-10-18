def as_xml(self,parent):
        """Create vcard-tmp XML representation of the field.

        :Parameters:
            - `parent`: parent node for the element
        :Types:
            - `parent`: `libxml2.xmlNode`

        :return: xml node with the field data.
        :returntype: `libxml2.xmlNode`"""
        n=parent.newChild(None,"ORG",None)
        n.newTextChild(None,"ORGNAME",to_utf8(self.name))
        n.newTextChild(None,"ORGUNIT",to_utf8(self.unit))
        return n
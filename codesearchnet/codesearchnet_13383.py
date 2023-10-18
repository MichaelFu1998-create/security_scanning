def as_xml(self,parent):
        """Create vcard-tmp XML representation of the field.

        :Parameters:
            - `parent`: parent node for the element
        :Types:
            - `parent`: `libxml2.xmlNode`

        :return: xml node with the field data.
        :returntype: `libxml2.xmlNode`"""
        n=parent.newChild(None,"N",None)
        n.newTextChild(None,"FAMILY",to_utf8(self.family))
        n.newTextChild(None,"GIVEN",to_utf8(self.given))
        n.newTextChild(None,"MIDDLE",to_utf8(self.middle))
        n.newTextChild(None,"PREFIX",to_utf8(self.prefix))
        n.newTextChild(None,"SUFFIX",to_utf8(self.suffix))
        return n
def as_xml(self,parent):
        """Create vcard-tmp XML representation of the field.

        :Parameters:
            - `parent`: parent node for the element
        :Types:
            - `parent`: `libxml2.xmlNode`

        :return: xml node with the field data.
        :returntype: `libxml2.xmlNode`"""
        n=parent.newChild(None,self.name.upper(),None)
        if self.type:
            n.newTextChild(None,"TYPE",self.type)
        n.newTextChild(None,"CRED",binascii.b2a_base64(self.cred))
        return n
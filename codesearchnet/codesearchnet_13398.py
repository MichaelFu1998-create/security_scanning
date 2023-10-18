def as_xml(self,parent):
        """Create vcard-tmp XML representation of the field.

        :Parameters:
            - `parent`: parent node for the element
        :Types:
            - `parent`: `libxml2.xmlNode`

        :return: xml node with the field data.
        :returntype: `libxml2.xmlNode`"""
        n=parent.newChild(None,self.name.upper(),None)
        if self.uri:
            n.newTextChild(None,"EXTVAL",to_utf8(self.uri))
        elif self.phonetic:
            n.newTextChild(None,"PHONETIC",to_utf8(self.phonetic))
        else:
            n.newTextChild(None,"BINVAL",binascii.b2a_base64(self.sound))
        return n
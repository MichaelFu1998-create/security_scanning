def as_xml(self,parent):
        """Create vcard-tmp XML representation of the field.

        :Parameters:
            - `parent`: parent node for the element
        :Types:
            - `parent`: `libxml2.xmlNode`

        :return: xml node with the field data.
        :returntype: `libxml2.xmlNode`"""
        n=parent.newChild(None,"ADR",None)
        for t in ("home","work","postal","parcel","dom","intl","pref"):
            if t in self.type:
                n.newChild(None,t.upper(),None)
        n.newTextChild(None,"POBOX",to_utf8(self.pobox))
        n.newTextChild(None,"EXTADD",to_utf8(self.extadr))
        n.newTextChild(None,"STREET",to_utf8(self.street))
        n.newTextChild(None,"LOCALITY",to_utf8(self.locality))
        n.newTextChild(None,"REGION",to_utf8(self.region))
        n.newTextChild(None,"PCODE",to_utf8(self.pcode))
        n.newTextChild(None,"CTRY",to_utf8(self.ctry))
        return n
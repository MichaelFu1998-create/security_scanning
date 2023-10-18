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
        for l in self.lines:
            n.newTextChild(None,"LINE",l)
        return n
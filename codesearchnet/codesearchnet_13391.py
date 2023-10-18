def as_xml(self,parent):
        """Create vcard-tmp XML representation of the field.

        :Parameters:
            - `parent`: parent node for the element
        :Types:
            - `parent`: `libxml2.xmlNode`

        :return: xml node with the field data.
        :returntype: `libxml2.xmlNode`"""
        n=parent.newChild(None,"TEL",None)
        for t in ("home","work","voice","fax","pager","msg","cell","video",
                "bbs","modem","isdn","pcs","pref"):
            if t in self.type:
                n.newChild(None,t.upper(),None)
        n.newTextChild(None,"NUMBER",to_utf8(self.number))
        return n
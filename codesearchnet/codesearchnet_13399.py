def as_xml(self,parent):
        """Create vcard-tmp XML representation of the field.

        :Parameters:
            - `parent`: parent node for the element
        :Types:
            - `parent`: `libxml2.xmlNode`

        :return: xml node with the field data.
        :returntype: `libxml2.xmlNode`"""
        if self.value in ("public","private","confidental"):
            n=parent.newChild(None,self.name.upper(),None)
            n.newChild(None,self.value.upper(),None)
            return n
        return None
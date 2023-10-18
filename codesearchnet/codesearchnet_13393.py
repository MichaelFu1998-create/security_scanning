def as_xml(self,parent):
        """Create vcard-tmp XML representation of the field.

        :Parameters:
            - `parent`: parent node for the element
        :Types:
            - `parent`: `libxml2.xmlNode`

        :return: xml node with the field data.
        :returntype: `libxml2.xmlNode`"""
        n=parent.newChild(None,"GEO",None)
        n.newTextChild(None,"LAT",to_utf8(self.lat))
        n.newTextChild(None,"LON",to_utf8(self.lon))
        return n
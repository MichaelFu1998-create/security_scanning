def as_xml(self,parent):
        """
        Create XML representation of `self`.

        :Parameters:
            - `parent`: the element to which the created node should be linked to.
        :Types:
            - `parent`: `libxml2.xmlNode`

        :return: an XML node.
        :returntype: `libxml2.xmlNode`
        """
        n=parent.newChild(None,"status",None)
        n.setProp("code","%03i" % (self.code,))
        return n
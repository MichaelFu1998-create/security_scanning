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
        n=parent.newChild(None,"item",None)
        if self.actor:
            n.newTextChild(None,"actor",to_utf8(self.actor))
        if self.reason:
            n.newTextChild(None,"reason",to_utf8(self.reason))
        n.setProp("affiliation",to_utf8(self.affiliation))
        if self.role:
            n.setProp("role",to_utf8(self.role))
        if self.jid:
            n.setProp("jid",to_utf8(self.jid.as_unicode()))
        if self.nick:
            n.setProp("nick",to_utf8(self.nick))
        return n
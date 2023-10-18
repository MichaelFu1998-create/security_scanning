def __from_xmlnode(self, xmlnode):
        """Initialize a `MucItem` object from an XML node.

        :Parameters:
            - `xmlnode`: the XML node.
        :Types:
            - `xmlnode`: `libxml2.xmlNode`
        """
        actor=None
        reason=None
        n=xmlnode.children
        while n:
            ns=n.ns()
            if ns and ns.getContent()!=MUC_USER_NS:
                continue
            if n.name=="actor":
                actor=n.getContent()
            if n.name=="reason":
                reason=n.getContent()
            n=n.next
        self.__init(
            from_utf8(xmlnode.prop("affiliation")),
            from_utf8(xmlnode.prop("role")),
            from_utf8(xmlnode.prop("jid")),
            from_utf8(xmlnode.prop("nick")),
            from_utf8(actor),
            from_utf8(reason),
            );
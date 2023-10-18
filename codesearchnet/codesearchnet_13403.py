def __from_xml(self,data):
        """Initialize a VCard object from XML node.

        :Parameters:
            - `data`: vcard to parse.
        :Types:
            - `data`: `libxml2.xmlNode`"""
        ns=get_node_ns(data)
        if ns and ns.getContent()!=VCARD_NS:
            raise ValueError("Not in the %r namespace" % (VCARD_NS,))
        if data.name!="vCard":
            raise ValueError("Bad root element name: %r" % (data.name,))
        n=data.children
        dns=get_node_ns(data)
        while n:
            if n.type!='element':
                n=n.next
                continue
            ns=get_node_ns(n)
            if (ns and dns and ns.getContent()!=dns.getContent()):
                n=n.next
                continue
            if not self.components.has_key(n.name):
                n=n.next
                continue
            cl,tp=self.components[n.name]
            if tp in ("required","optional"):
                if self.content.has_key(n.name):
                    raise ValueError("Duplicate %s" % (n.name,))
                try:
                    self.content[n.name]=cl(n.name,n)
                except Empty:
                    pass
            elif tp=="multi":
                if not self.content.has_key(n.name):
                    self.content[n.name]=[]
                try:
                    self.content[n.name].append(cl(n.name,n))
                except Empty:
                    pass
            n=n.next
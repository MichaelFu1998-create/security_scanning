def from_xml(self,xmlnode):
        """Initialize Delay object from an XML node.

        :Parameters:
            - `xmlnode`: the jabber:x:delay XML element.
        :Types:
            - `xmlnode`: `libxml2.xmlNode`"""
        if xmlnode.type!="element":
            raise ValueError("XML node is not a jabber:x:delay element (not an element)")
        ns=get_node_ns_uri(xmlnode)
        if ns and ns!=DELAY_NS or xmlnode.name!="x":
            raise ValueError("XML node is not a jabber:x:delay element")
        stamp=xmlnode.prop("stamp")
        if stamp.endswith("Z"):
            stamp=stamp[:-1]
        if "-" in stamp:
            stamp=stamp.split("-",1)[0]
        try:
            tm = time.strptime(stamp, "%Y%m%dT%H:%M:%S")
        except ValueError:
            raise BadRequestProtocolError("Bad timestamp")
        tm=tm[0:8]+(0,)
        self.timestamp=datetime.datetime.fromtimestamp(time.mktime(tm))
        delay_from=from_utf8(xmlnode.prop("from"))
        if delay_from:
            try:
                self.delay_from = JID(delay_from)
            except JIDError:
                raise JIDMalformedProtocolError("Bad JID in the jabber:x:delay 'from' attribute")
        else:
            self.delay_from = None
        self.reason = from_utf8(xmlnode.getContent())
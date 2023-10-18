def __from_xml(self,value):
        """Initialize a `VCardAdr` object from and XML element.

        :Parameters:
            - `value`: field value as an XML node
        :Types:
            - `value`: `libxml2.xmlNode`"""
        n=value.children
        vns=get_node_ns(value)
        while n:
            if n.type!='element':
                n=n.next
                continue
            ns=get_node_ns(n)
            if (ns and vns and ns.getContent()!=vns.getContent()):
                n=n.next
                continue
            if n.name=='POBOX':
                self.pobox=unicode(n.getContent(),"utf-8","replace")
            elif n.name in ('EXTADR', 'EXTADD'):
                self.extadr=unicode(n.getContent(),"utf-8","replace")
            elif n.name=='STREET':
                self.street=unicode(n.getContent(),"utf-8","replace")
            elif n.name=='LOCALITY':
                self.locality=unicode(n.getContent(),"utf-8","replace")
            elif n.name=='REGION':
                self.region=unicode(n.getContent(),"utf-8","replace")
            elif n.name=='PCODE':
                self.pcode=unicode(n.getContent(),"utf-8","replace")
            elif n.name=='CTRY':
                self.ctry=unicode(n.getContent(),"utf-8","replace")
            elif n.name in ("HOME","WORK","POSTAL","PARCEL","DOM","INTL",
                    "PREF"):
                self.type.append(n.name.lower())
            n=n.next
        if self.type==[]:
            self.type=["intl","postal","parcel","work"]
        elif "dom" in self.type and "intl" in self.type:
            raise ValueError("Both 'dom' and 'intl' specified in vcard ADR")
def _process_rfc2425_record(self,data):
        """Parse single RFC2425 record and update attributes of `self`.

        :Parameters:
            - `data`: the record (probably multiline)
        :Types:
            - `data`: `unicode`"""
        label,value=data.split(":",1)
        value=value.replace("\\n","\n").replace("\\N","\n")
        psplit=label.lower().split(";")
        name=psplit[0]
        params=psplit[1:]
        if u"." in name:
            name=name.split(".",1)[1]
        name=name.upper()
        if name in (u"X-DESC",u"X-JABBERID"):
            name=name[2:]
        if not self.components.has_key(name):
            return
        if params:
            params=dict([p.split("=",1) for p in params])
        cl,tp=self.components[name]
        if tp in ("required","optional"):
            if self.content.has_key(name):
                raise ValueError("Duplicate %s" % (name,))
            try:
                self.content[name]=cl(name,value,params)
            except Empty:
                pass
        elif tp=="multi":
            if not self.content.has_key(name):
                self.content[name]=[]
            try:
                self.content[name].append(cl(name,value,params))
            except Empty:
                pass
        else:
            return
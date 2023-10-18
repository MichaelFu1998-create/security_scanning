def __from_rfc2426(self,data):
        """Initialize a VCard object from an RFC2426 string.

        :Parameters:
            - `data`: vcard to parse.
        :Types:
            - `data`: `libxml2.xmlNode`, `unicode` or `str`"""
        data=from_utf8(data)
        lines=data.split("\n")
        started=0
        current=None
        for l in lines:
            if not l:
                continue
            if l[-1]=="\r":
                l=l[:-1]
            if not l:
                continue
            if l[0] in " \t":
                if current is None:
                    continue
                current+=l[1:]
                continue
            if not started and current and current.upper().strip()=="BEGIN:VCARD":
                started=1
            elif started and current.upper().strip()=="END:VCARD":
                current=None
                break
            elif current and started:
                self._process_rfc2425_record(current)
            current=l
        if started and current:
            self._process_rfc2425_record(current)
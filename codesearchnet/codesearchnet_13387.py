def rfc2426(self):
        """RFC2426-encode the field content.

        :return: the field in the RFC 2426 format.
        :returntype: `str`"""
        return rfc2425encode("adr",u';'.join(quote_semicolon(val) for val in
                (self.pobox,self.extadr,self.street,self.locality,
                        self.region,self.pcode,self.ctry)),
                {"type":",".join(self.type)})
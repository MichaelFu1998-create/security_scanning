def rfc2426(self):
        """RFC2426-encode the field content.

        :return: the field in the RFC 2426 format.
        :returntype: `str`"""
        if self.unit:
            return rfc2425encode("org",u';'.join(quote_semicolon(val) for val in
                                      (self.name,self.unit)))
        else:
            return rfc2425encode("org",unicode(quote_semicolon(self.name)))
def rfc2426(self):
        """RFC2426-encode the field content.

        :return: the field in the RFC 2426 format.
        :returntype: `str`"""
        return rfc2425encode("n",u';'.join(quote_semicolon(val) for val in
                (self.family,self.given,self.middle,self.prefix,self.suffix)))
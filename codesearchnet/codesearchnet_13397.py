def rfc2426(self):
        """RFC2426-encode the field content.

        :return: the field in the RFC 2426 format.
        :returntype: `str`"""
        if self.uri:
            return rfc2425encode(self.name,self.uri,{"value":"uri"})
        elif self.sound:
            return rfc2425encode(self.name,self.sound)
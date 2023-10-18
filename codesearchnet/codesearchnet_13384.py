def rfc2426(self):
        """RFC2426-encode the field content.

        :return: the field in the RFC 2426 format.
        :returntype: `str`"""
        if self.uri:
            return rfc2425encode(self.name,self.uri,{"value":"uri"})
        elif self.image:
            if self.type:
                p={"type":self.type}
            else:
                p={}
            return rfc2425encode(self.name,self.image,p)
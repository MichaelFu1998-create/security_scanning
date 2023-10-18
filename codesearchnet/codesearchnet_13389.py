def rfc2426(self):
        """RFC2426-encode the field content.

        :return: the field in the RFC 2426 format.
        :returntype: `str`"""
        return rfc2425encode("label",u"\n".join(self.lines),
                {"type":",".join(self.type)})
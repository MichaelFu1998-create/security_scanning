def rfc2426(self):
        """Get the RFC2426 representation of `self`.

        :return: the UTF-8 encoded RFC2426 representation.
        :returntype: `str`"""
        ret="begin:VCARD\r\n"
        ret+="version:3.0\r\n"
        for _unused, value in self.content.items():
            if value is None:
                continue
            if type(value) is list:
                for v in value:
                    ret+=v.rfc2426()
            else:
                v=value.rfc2426()
                ret+=v
        return ret+"end:VCARD\r\n"
def get_href(self):
        """Convert path to a URL that can be passed to XML responses.

        Byte string, UTF-8 encoded, quoted.

        See http://www.webdav.org/specs/rfc4918.html#rfc.section.8.3
        We are using the path-absolute option. i.e. starting with '/'.
        URI ; See section 3.2.1 of [RFC2068]
        """
        # Nautilus chokes, if href encodes '(' as '%28'
        # So we don't encode 'extra' and 'safe' characters (see rfc2068 3.2.1)
        safe = "/" + "!*'()," + "$-_|."
        return compat.quote(
            self.provider.mount_path
            + self.provider.share_path
            + self.get_preferred_path(),
            safe=safe,
        )
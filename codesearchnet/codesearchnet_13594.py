def as_unicode(self):
        """Unicode string JID representation.

        :return: JID as Unicode string."""
        result = self.domain
        if self.local:
            result = self.local + u'@' + result
        if self.resource:
            result = result + u'/' + self.resource
        if not JID.cache.has_key(result):
            JID.cache[result] = self
        return result
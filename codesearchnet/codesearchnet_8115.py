def extract(self, msg):
        """Yield an ordered dictionary if msg['type'] is in keys_by_type."""
        def normal(key):
            v = msg.get(key)
            if v is None:
                return v
            normalizer = self.normalizers.get(key, lambda x: x)
            return normalizer(v)

        def odict(keys):
            return collections.OrderedDict((k, normal(k)) for k in keys)

        def match(m):
            return (msg.get(k) in v for k, v in m.items()) if m else ()

        accept = all(match(self.accept))
        reject = any(match(self.reject))

        if reject or not accept:
            keys = ()
        elif self.keys_by_type is None:
            keys = [k for k in msg.keys() if k not in self.omit]
        else:
            keys = self.keys_by_type.get(msg.get('type'))
        return odict(keys)
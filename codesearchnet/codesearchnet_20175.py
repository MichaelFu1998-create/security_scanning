def delete_keys(self, *args, **kwargs):
        """Remove each key or key name in an iterable from the bucket set.
        """
        ikeys = iter(kwargs.get('keys', args[0] if args else []))

        while True:
            try:
                key = ikeys.next()
            except StopIteration:
                break

            if isinstance(key, basestring):
                mimicdb.backend.srem(tpl.bucket % self.name, key)
                mimicdb.backend.delete(tpl.key % (self.name, key))
            elif isinstance(key, BotoKey) or isinstance(key, Key):
                mimicdb.backend.srem(tpl.bucket % self.name, key.name)
                mimicdb.backend.delete(tpl.key % (self.name, key.name))

        return super(Bucket, self).delete_keys(*args, **kwargs)
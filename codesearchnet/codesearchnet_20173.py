def _get_key_internal(self, *args, **kwargs):
        """Return None if key is not in the bucket set.

        Pass 'force' in the headers to check S3 for the key, and after fetching
        the key from S3, save the metadata and key to the bucket set.
        """
        if args[1] is not None and 'force' in args[1]:
            key, res = super(Bucket, self)._get_key_internal(*args, **kwargs)

            if key:
                mimicdb.backend.sadd(tpl.bucket % self.name, key.name)
                mimicdb.backend.hmset(tpl.key % (self.name, key.name),
                                    dict(size=key.size,
                                         md5=key.etag.strip('"')))
            return key, res

        key = None

        if mimicdb.backend.sismember(tpl.bucket % self.name, args[0]):
            key = Key(self)
            key.name = args[0]

        return key, None
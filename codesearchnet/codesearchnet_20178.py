def _get_all(self, *args, **kwargs):
        """If 'force' is in the headers, retrieve the list of keys from S3.
        Otherwise, use the list() function to retrieve the keys from MimicDB.
        """
        headers = kwargs.get('headers', args[2] if len(args) > 2 else None) or dict()

        if 'force' in headers:
            keys = super(Bucket, self)._get_all(*args, **kwargs)

            for key in keys:
                mimicdb.backend.sadd(tpl.bucket % self.name, key.name)
                mimicdb.backend.hmset(tpl.key % (self.name, key.name), dict(size=key.size, md5=key.etag.strip('"')))

                key.name = key.name

            return keys

        prefix = kwargs.get('prefix', '')

        return list(self.list(prefix=prefix))
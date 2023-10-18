def list(self, *args, **kwargs):
        """Return an iterable of keys from MimicDB.

        :param boolean force: If true, API call is forced to S3
        """
        if kwargs.pop('force', None):
            headers = kwargs.get('headers', args[4] if len(args) > 4 else None) or dict()
            headers['force'] = True
            kwargs['headers'] = headers

            for key in super(Bucket, self).list(*args, **kwargs):
                yield key

        else:
            prefix = kwargs.get('prefix', args[0] if args else '')

            for key in mimicdb.backend.smembers(tpl.bucket % self.name):
                if key.startswith(prefix):
                    k = Key(self, key)

                    meta = mimicdb.backend.hgetall(tpl.key % (self.name, key))

                    if meta:
                        k._load_meta(meta['size'], meta['md5'])

                    yield k
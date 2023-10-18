def name(self, value):
        """Key name can be set by Key.key or Key.name. Key.key sets Key.name
        internally, so just handle this property. When changing the key
        name, try to load it's metadata from MimicDB. If it's not available,
        the key hasn't been uploaded, downloaded or synced so don't add it to
        the bucket set (it also might have just been deleted,
        see boto.s3.bucket.py#785)
        """
        self._name = value

        if value:
            meta = mimicdb.backend.hgetall(tpl.key % (self.bucket.name, value))

            if meta:
                mimicdb.backend.sadd(tpl.bucket % self.bucket.name, value)
                self._load_meta(meta['size'], meta['md5'])
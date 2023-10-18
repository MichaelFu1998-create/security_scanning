def _send_file_internal(self, *args, **kwargs):
        """Called internally for any type of upload. After upload finishes,
        make sure the key is in the bucket set and save the metadata.
        """
        super(Key, self)._send_file_internal(*args, **kwargs)

        mimicdb.backend.sadd(tpl.bucket % self.bucket.name, self.name)
        mimicdb.backend.hmset(tpl.key % (self.bucket.name, self.name),
                            dict(size=self.size, md5=self.md5))
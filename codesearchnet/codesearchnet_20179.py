def sync(self):
        """Sync a bucket.

        Force all API calls to S3 and populate the database with the current state of S3.
        """
        for key in mimicdb.backend.smembers(tpl.bucket % self.name):
            mimicdb.backend.delete(tpl.key % (self.name, key))

        mimicdb.backend.delete(tpl.bucket % self.name)
        mimicdb.backend.sadd(tpl.connection, self.name)

        for key in self.list(force=True):
            mimicdb.backend.sadd(tpl.bucket % self.name, key.name)
            mimicdb.backend.hmset(tpl.key % (self.name, key.name), dict(size=key.size, md5=key.etag.strip('"')))
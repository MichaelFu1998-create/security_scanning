def sync(self, *buckets):
        """Sync either a list of buckets or the entire connection.

        Force all API calls to S3 and populate the database with the current
        state of S3.

        :param \*string \*buckets: Buckets to sync
        """
        if buckets:
            for _bucket in buckets:
                for key in mimicdb.backend.smembers(tpl.bucket % _bucket):
                    mimicdb.backend.delete(tpl.key % (_bucket, key))

                mimicdb.backend.delete(tpl.bucket % _bucket)

                bucket = self.get_bucket(_bucket, force=True)

                for key in bucket.list(force=True):
                    mimicdb.backend.sadd(tpl.bucket % bucket.name, key.name)
                    mimicdb.backend.hmset(tpl.key % (bucket.name, key.name), dict(size=key.size, md5=key.etag.strip('"')))
        else:
            for bucket in mimicdb.backend.smembers(tpl.connection):
                for key in mimicdb.backend.smembers(tpl.bucket % bucket):
                    mimicdb.backend.delete(tpl.key % (bucket, key))

                mimicdb.backend.delete(tpl.bucket % bucket)

            for bucket in self.get_all_buckets(force=True):
                for key in bucket.list(force=True):
                    mimicdb.backend.sadd(tpl.bucket % bucket.name, key.name)
                    mimicdb.backend.hmset(tpl.key % (bucket.name, key.name), dict(size=key.size, md5=key.etag.strip('"')))
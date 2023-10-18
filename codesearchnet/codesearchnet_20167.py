def get_all_buckets(self, *args, **kwargs):
        """Return a list of buckets in MimicDB.

        :param boolean force: If true, API call is forced to S3
        """
        if kwargs.pop('force', None):
            buckets = super(S3Connection, self).get_all_buckets(*args, **kwargs)

            for bucket in buckets:
                mimicdb.backend.sadd(tpl.connection, bucket.name)

            return buckets

        return [Bucket(self, bucket) for bucket in mimicdb.backend.smembers(tpl.connection)]
def create_bucket(self, *args, **kwargs):
        """Add the bucket to MimicDB after successful creation.
        """
        bucket = super(S3Connection, self).create_bucket(*args, **kwargs)

        if bucket:
            mimicdb.backend.sadd(tpl.connection, bucket.name)

        return bucket
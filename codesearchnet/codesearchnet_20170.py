def delete_bucket(self, *args, **kwargs):
        """Delete the bucket on S3 before removing it from MimicDB.
        If the delete fails (usually because the bucket is not empty), do
        not remove the bucket from the set.
        """
        super(S3Connection, self).delete_bucket(*args, **kwargs)

        bucket = kwargs.get('bucket_name', args[0] if args else None)

        if bucket:
            mimicdb.backend.srem(tpl.connection, bucket)
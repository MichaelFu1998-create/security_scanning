def get_bucket(self, bucket_name, validate=True, headers=None, force=None):
        """Return a bucket from MimicDB if it exists. Return a
        S3ResponseError if the bucket does not exist and validate is passed.

        :param boolean force: If true, API call is forced to S3
        """
        if force:
            bucket = super(S3Connection, self).get_bucket(bucket_name, validate, headers)
            mimicdb.backend.sadd(tpl.connection, bucket.name)
            return bucket

        if mimicdb.backend.sismember(tpl.connection, bucket_name):
            return Bucket(self, bucket_name)
        else:
            if validate:
                raise S3ResponseError(404, 'NoSuchBucket')
            else:
                return Bucket(self, bucket_name)
def get_key(self, *args, **kwargs):
        """Return the key from MimicDB.

        :param boolean force: If true, API call is forced to S3
        """
        if kwargs.pop('force', None):
            headers = kwargs.get('headers', {})
            headers['force'] = True
            kwargs['headers'] = headers

        return super(Bucket, self).get_key(*args, **kwargs)
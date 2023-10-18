def get_all_keys(self, *args, **kwargs):
        """Return a list of keys from MimicDB.

        :param boolean force: If true, API call is forced to S3
        """
        if kwargs.pop('force', None):
            headers = kwargs.get('headers', args[0] if len(args) else None) or dict()
            headers['force'] = True
            kwargs['headers'] = headers

        return super(Bucket, self).get_all_keys(*args, **kwargs)
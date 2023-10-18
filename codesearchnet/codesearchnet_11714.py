def invalidate(self, *paths):
        """
        Issues invalidation requests to a Cloudfront distribution
        for the current static media bucket, triggering it to reload the specified
        paths from the origin.

        Note, only 1000 paths can be issued in a request at any one time.
        """
        dj = self.get_satchel('dj')
        if not paths:
            return
        # http://boto.readthedocs.org/en/latest/cloudfront_tut.html
        _settings = dj.get_settings()
        if not _settings.AWS_STATIC_BUCKET_NAME:
            print('No static media bucket set.')
            return
        if isinstance(paths, six.string_types):
            paths = paths.split(',')
        all_paths = map(str.strip, paths)
        i = 0
        while 1:
            paths = all_paths[i:i+1000]
            if not paths:
                break

            c = boto.connect_cloudfront()
            rs = c.get_all_distributions()
            target_dist = None
            for dist in rs:
                print(dist.domain_name, dir(dist), dist.__dict__)
                bucket_name = dist.origin.dns_name.replace('.s3.amazonaws.com', '')
                if bucket_name == _settings.AWS_STATIC_BUCKET_NAME:
                    target_dist = dist
                    break
            if not target_dist:
                raise Exception(('Target distribution %s could not be found in the AWS account.') % (settings.AWS_STATIC_BUCKET_NAME,))
            print('Using distribution %s associated with origin %s.' % (target_dist.id, _settings.AWS_STATIC_BUCKET_NAME))
            inval_req = c.create_invalidation_request(target_dist.id, paths)
            print('Issue invalidation request %s.' % (inval_req,))
            i += 1000
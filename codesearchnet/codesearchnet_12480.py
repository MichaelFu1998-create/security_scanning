def _load_info(self):
        '''Get user info for GBDX S3, put into instance vars for convenience.

        Args:
            None.

        Returns:
            Dictionary with S3 access key, S3 secret key, S3 session token,
            user bucket and user prefix (dict).
        '''

        url = '%s/prefix?duration=36000' % self.base_url
        r = self.gbdx_connection.get(url)
        r.raise_for_status()
        return r.json()
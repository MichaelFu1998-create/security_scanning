def amz_cano_path(self, path):
        """
        Generate the canonical path as per AWS4 auth requirements.

        Not documented anywhere, determined from aws4_testsuite examples,
        problem reports and testing against the live services.

        path -- request path

        """
        safe_chars = '/~'
        qs = ''
        fixed_path = path
        if '?' in fixed_path:
            fixed_path, qs = fixed_path.split('?', 1)
        fixed_path = posixpath.normpath(fixed_path)
        fixed_path = re.sub('/+', '/', fixed_path)
        if path.endswith('/') and not fixed_path.endswith('/'):
            fixed_path += '/'
        full_path = fixed_path
        # If Python 2, switch to working entirely in str as quote() has problems
        # with Unicode
        if PY2:
            full_path = full_path.encode('utf-8')
            safe_chars = safe_chars.encode('utf-8')
            qs = qs.encode('utf-8')
        # S3 seems to require unquoting first. 'host' service is used in
        # amz_testsuite tests
        if self.service in ['s3', 'host']:
            full_path = unquote(full_path)
        full_path = quote(full_path, safe=safe_chars)
        if qs:
            qm = b'?' if PY2 else '?'
            full_path = qm.join((full_path, qs))
        if PY2:
            full_path = unicode(full_path)
        return full_path
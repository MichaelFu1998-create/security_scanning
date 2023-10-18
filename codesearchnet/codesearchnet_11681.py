def get_expiration_date(self, fn):
        """
        Reads the expiration date of a local crt file.
        """
        r = self.local_renderer
        r.env.crt_fn = fn
        with hide('running'):
            ret = r.local('openssl x509 -noout -in {ssl_crt_fn} -dates', capture=True)
        matches = re.findall('notAfter=(.*?)$', ret, flags=re.IGNORECASE)
        if matches:
            return dateutil.parser.parse(matches[0])
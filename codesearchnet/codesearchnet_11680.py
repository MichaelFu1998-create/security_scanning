def generate_csr(self, domain='', r=None):
        """
        Creates a certificate signing request to be submitted to a formal
        certificate authority to generate a certificate.

        Note, the provider may say the CSR must be created on the target server,
        but this is not necessary.
        """
        r = r or self.local_renderer
        r.env.domain = domain or r.env.domain
        role = self.genv.ROLE or ALL
        site = self.genv.SITE or self.genv.default_site
        print('self.genv.default_site:', self.genv.default_site, file=sys.stderr)
        print('site.csr0:', site, file=sys.stderr)
        ssl_dst = 'roles/%s/ssl' % (role,)
        print('ssl_dst:', ssl_dst)
        if not os.path.isdir(ssl_dst):
            os.makedirs(ssl_dst)
        for site, site_data in self.iter_sites():
            print('site.csr1:', site, file=sys.stderr)
            assert r.env.domain, 'No SSL domain defined.'
            r.env.ssl_base_dst = '%s/%s' % (ssl_dst, r.env.domain.replace('*.', ''))
            r.env.ssl_csr_year = date.today().year
            r.local('openssl req -nodes -newkey rsa:{ssl_length} '
                '-subj "/C={ssl_country}/ST={ssl_state}/L={ssl_city}/O={ssl_organization}/CN={ssl_domain}" '
                '-keyout {ssl_base_dst}.{ssl_csr_year}.key -out {ssl_base_dst}.{ssl_csr_year}.csr')
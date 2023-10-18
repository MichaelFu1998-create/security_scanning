def generate_self_signed_certificate(self, domain='', r=None):
        """
        Generates a self-signed certificate for use in an internal development
        environment for testing SSL pages.

        http://almostalldigital.wordpress.com/2013/03/07/self-signed-ssl-certificate-for-ec2-load-balancer/
        """
        r = self.local_renderer
        r.env.domain = domain or r.env.domain
        assert r.env.domain, 'No SSL domain defined.'
        role = r or self.genv.ROLE or ALL
        ssl_dst = 'roles/%s/ssl' % (role,)
        if not os.path.isdir(ssl_dst):
            os.makedirs(ssl_dst)
        r.env.base_dst = '%s/%s' % (ssl_dst, r.env.domain)
        r.local('openssl req -new -newkey rsa:{ssl_length} '
            '-days {ssl_days} -nodes -x509 '
            '-subj "/C={ssl_country}/ST={ssl_state}/L={ssl_city}/O={ssl_organization}/CN={ssl_domain}" '
            '-keyout {ssl_base_dst}.key -out {ssl_base_dst}.crt')
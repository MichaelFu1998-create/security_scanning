def verify_certificate_chain(self, base=None, crt=None, csr=None, key=None):
        """
        Confirms the key, CSR, and certificate files all match.
        """
        from burlap.common import get_verbose, print_fail, print_success

        r = self.local_renderer

        if base:
            crt = base + '.crt'
            csr = base + '.csr'
            key = base + '.key'
        else:
            assert crt and csr and key, 'If base not provided, crt and csr and key must be given.'

        assert os.path.isfile(crt)
        assert os.path.isfile(csr)
        assert os.path.isfile(key)

        csr_md5 = r.local('openssl req -noout -modulus -in %s | openssl md5' % csr, capture=True)
        key_md5 = r.local('openssl rsa -noout -modulus -in %s | openssl md5' % key, capture=True)
        crt_md5 = r.local('openssl x509 -noout -modulus -in %s | openssl md5' % crt, capture=True)

        match = crt_md5 == csr_md5 == key_md5

        if self.verbose or not match:
            print('crt:', crt_md5)
            print('csr:', csr_md5)
            print('key:', key_md5)

        if match:
            print_success('Files look good!')
        else:
            print_fail('Files no not match!')
            raise Exception('Files no not match!')
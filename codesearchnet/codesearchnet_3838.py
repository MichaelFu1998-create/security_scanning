def expired(self, cfgstr=None, product=None):
        """
        Check to see if a previously existing stamp is still valid and if the
        expected result of that computation still exists.

        Args:
            cfgstr (str, optional): override the default cfgstr if specified
            product (PathLike or Sequence[PathLike], optional): override the
                default product if specified
        """
        products = self._rectify_products(product)
        certificate = self._get_certificate(cfgstr=cfgstr)
        if certificate is None:
            # We dont have a certificate, so we are expired
            is_expired = True
        elif products is None:
            # We dont have a product to check, so assume not expired
            is_expired = False
        elif not all(map(os.path.exists, products)):
            # We are expired if the expected product does not exist
            is_expired = True
        else:
            # We are expired if the hash of the existing product data
            # does not match the expected hash in the certificate
            product_file_hash = self._product_file_hash(products)
            certificate_hash = certificate.get('product_file_hash', None)
            is_expired = product_file_hash != certificate_hash
        return is_expired
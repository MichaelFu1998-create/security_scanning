def renew(self, cfgstr=None, product=None):
        """
        Recertify that the product has been recomputed by writing a new
        certificate to disk.
        """
        products = self._rectify_products(product)
        certificate = {
            'timestamp': util_time.timestamp(),
            'product': products,
        }
        if products is not None:
            if not all(map(os.path.exists, products)):
                raise IOError(
                    'The stamped product must exist: {}'.format(products))
            certificate['product_file_hash'] = self._product_file_hash(products)
        self.cacher.save(certificate, cfgstr=cfgstr)
        return certificate
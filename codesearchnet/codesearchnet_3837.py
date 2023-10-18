def _product_file_hash(self, product=None):
        """
        Get the hash of the each product file
        """
        if self.hasher is None:
            return None
        else:
            products = self._rectify_products(product)
            product_file_hash = [
                util_hash.hash_file(p, hasher=self.hasher, base='hex')
                for p in products
            ]
            return product_file_hash
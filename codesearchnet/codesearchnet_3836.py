def _rectify_products(self, product=None):
        """ puts products in a normalized format """
        products = self.product if product is None else product
        if products is None:
            return None
        if not isinstance(products, (list, tuple)):
            products = [products]
        return products
def delete(self, store_id, cart_id, line_id):
        """
        Delete a cart.

        :param store_id: The store id.
        :type store_id: :py:class:`str`
        :param cart_id: The id for the cart.
        :type cart_id: :py:class:`str`
        :param line_id: The id for the line item of a cart.
        :type line_id: :py:class:`str`
        """
        self.store_id = store_id
        self.cart_id = cart_id
        self.line_id = line_id
        return self._mc_client._delete(url=self._build_path(store_id, 'carts', cart_id, 'lines', line_id))
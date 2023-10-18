def get_abi(self, hsh: bytes) -> Dict[str, Any]:
        """Returns a copy of the Solidity JSON ABI item for the function associated with the selector ``hsh``.

        If no normal contract function has the specified selector, a dict describing the default or non-default
        fallback function is returned.

        The content of the returned dict is described at https://solidity.readthedocs.io/en/latest/abi-spec.html#json_
        """
        if not isinstance(hsh, (bytes, bytearray)):
            raise TypeError('The selector argument must be a concrete byte array')
        sig = self._function_signatures_by_selector.get(hsh)
        if sig is not None:
            return dict(self._function_abi_items_by_signature[sig])
        item = self._fallback_function_abi_item
        if item is not None:
            return dict(item)
        # An item describing the default fallback function.
        return {'payable': False, 'stateMutability': 'nonpayable', 'type': 'fallback'}
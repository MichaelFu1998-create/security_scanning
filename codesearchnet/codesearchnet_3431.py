def get_func_return_types(self, hsh: bytes) -> str:
        """Returns the tuple type signature for the output values of the function
        associated with the selector ``hsh``.

        If no normal contract function has the specified selector,
        the empty tuple type signature ``'()'`` is returned.
        """
        if not isinstance(hsh, (bytes, bytearray)):
            raise TypeError('The selector argument must be a concrete byte array')
        abi = self.get_abi(hsh)
        outputs = abi.get('outputs')
        return '()' if outputs is None else SolidityMetadata.tuple_signature_for_components(outputs)
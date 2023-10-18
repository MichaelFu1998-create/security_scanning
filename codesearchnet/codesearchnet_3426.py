def get_constructor_arguments(self) -> str:
        """Returns the tuple type signature for the arguments of the contract constructor."""
        item = self._constructor_abi_item
        return '()' if item is None else self.tuple_signature_for_components(item['inputs'])
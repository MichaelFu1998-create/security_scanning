def function_selectors(self) -> Iterable[bytes]:
        """The selectors of all normal contract functions,
        plus ``self.fallback_function_selector`` if the contract has a non-default fallback function.
        """
        selectors = self._function_signatures_by_selector.keys()
        if self._fallback_function_abi_item is None:
            return tuple(selectors)
        return (*selectors, self.fallback_function_selector)
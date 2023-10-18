def hashes(self) -> Tuple[bytes, ...]:
        """The selectors of all normal contract functions, plus ``self.fallback_function_selector``."""
        selectors = self._function_signatures_by_selector.keys()
        return (*selectors, self.fallback_function_selector)
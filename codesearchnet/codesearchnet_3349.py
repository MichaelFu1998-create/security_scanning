def _hook_unmapped(self, uc, access, address, size, value, data):
        """
        We hit an unmapped region; map it into unicorn.
        """

        try:
            m = self._create_emulated_mapping(uc, address)
        except MemoryException as e:
            self._to_raise = e
            self._should_try_again = False
            return False

        self._should_try_again = True
        return False
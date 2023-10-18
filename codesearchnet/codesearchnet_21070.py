def get_modes(self):
        """Get the modes supported by this device."""
        if not self.__modes:
            self.__modes = yield from self.handle_list(
                self.API.get('valid_modes'))

        return self.__modes
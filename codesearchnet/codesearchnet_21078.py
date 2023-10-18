def get_equalisers(self):
        """Get the equaliser modes supported by this device."""
        if not self.__equalisers:
            self.__equalisers = yield from self.handle_list(
                self.API.get('equalisers'))

        return self.__equalisers
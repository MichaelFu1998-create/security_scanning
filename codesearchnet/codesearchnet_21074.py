def get_volume_steps(self):
        """Read the maximum volume level of the device."""
        if not self.__volume_steps:
            self.__volume_steps = yield from self.handle_int(
                self.API.get('volume_steps'))

        return self.__volume_steps
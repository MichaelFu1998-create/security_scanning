def get_mode_list(self):
        """Get the label list of the supported modes."""
        self.__modes = yield from self.get_modes()
        return (yield from self.collect_labels(self.__modes))
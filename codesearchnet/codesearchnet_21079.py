def get_equaliser_list(self):
        """Get the label list of the supported modes."""
        self.__equalisers = yield from self.get_equalisers()
        return (yield from self.collect_labels(self.__equalisers))
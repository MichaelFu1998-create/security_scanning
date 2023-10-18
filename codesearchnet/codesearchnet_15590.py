def _signal_handler_map(self):
        """ Create the signal handler map

        create a dictionary with signal:handler mapping based on
        self.signal_map

        :return: dict
        """
        result = {}
        for signum, handler in self.signal_map.items():
            result[signum] = self._get_signal_handler(handler)
        return result
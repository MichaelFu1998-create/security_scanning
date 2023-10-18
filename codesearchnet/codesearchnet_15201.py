def value(self):
        """
        Internal use only.
        """
        if not self._fix["beta"]:
            self._update_beta()

        if not self._fix["scale"]:
            self._update_scale()

        return self.lml()
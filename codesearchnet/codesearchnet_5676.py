def pop_marker(self, reset):
        """ Pop a marker off of the marker stack. If reset is True then the
        iterator will be returned to the state it was in before the
        corresponding call to push_marker().

        """

        saved = self.saved_markers.pop()

        if reset:
            self.marker = saved
        elif self.saved_markers:
            self.saved_markers[-1] = saved
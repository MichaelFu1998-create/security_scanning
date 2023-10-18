def pop_marker(self, reset):
        """ Pop a marker off of the marker stack. If reset is True then the
        iterator will be returned to the state it was in before the
        corresponding call to push_marker().

        """

        marker = self.markers.pop()

        if reset:
            # Make the values available to be read again
            marker.extend(self.look_ahead)
            self.look_ahead = marker
        elif self.markers:
            # Otherwise, reassign the values to the top marker
            self.markers[-1].extend(marker)
        else:
            # If there are not more markers in the stack then discard the values
            pass
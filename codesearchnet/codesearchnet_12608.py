def set_volume(self, volume):
        """
        Args:
            float: volume in the interval [0, 10]
        """
        # 0 isn't handled correctly so we have to set it to a very small value to achieve the same purpose
        if volume == 0:
            volume = 1e-10
        return self._player_interface_property('Volume', dbus.Double(volume))
def set_rate(self, rate):
        """
        Set the playback rate of the video as a multiple of the default playback speed

        Examples:
            >>> player.set_rate(2)
            # Will play twice as fast as normal speed
            >>> player.set_rate(0.5)
            # Will play half speed
        """
        self._rate = self._player_interface_property('Rate', dbus.Double(rate))
        return self._rate
def set_position(self, position):
        """
        Set the video to playback position to `position` seconds from the start of the video

        Args:
            position (float): The position in seconds.
        """
        self._player_interface.SetPosition(ObjectPath("/not/used"), Int64(position * 1000.0 * 1000))
        self.positionEvent(self, position)
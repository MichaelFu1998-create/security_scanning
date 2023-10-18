def seek(self, relative_position):
        """
        Seek the video by `relative_position` seconds

        Args:
            relative_position (float): The position in seconds to seek to.
        """
        self._player_interface.Seek(Int64(1000.0 * 1000 * relative_position))
        self.seekEvent(self, relative_position)
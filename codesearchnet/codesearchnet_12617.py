def is_playing(self):
        """
        Returns:
            bool: Whether the player is playing
        """
        self._is_playing = (self.playback_status() == "Playing")
        logger.info("Playing?: %s" % self._is_playing)
        return self._is_playing
def pause(self):
        """
        Pause playback
        """
        self._player_interface.Pause()
        self._is_playing = False
        self.pauseEvent(self)
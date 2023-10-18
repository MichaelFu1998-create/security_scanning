def play_pause(self):
        """
        Pause playback if currently playing, otherwise start playing if currently paused.
        """
        self._player_interface.PlayPause()
        self._is_playing = not self._is_playing
        if self._is_playing:
            self.playEvent(self)
        else:
            self.pauseEvent(self)
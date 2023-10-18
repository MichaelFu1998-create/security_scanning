def play(self):
        """
        Play the video asynchronously returning control immediately to the calling code
        """
        if not self.is_playing():
            self.play_pause()
            self._is_playing = True
            self.playEvent(self)
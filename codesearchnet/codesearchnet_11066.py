def pause(self):
        """Pause the music"""
        self.pause_time = self.get_time()
        self.paused = True
        self.player.pause()
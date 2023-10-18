def start(self):
        """Start the timer"""
        self.music.start()
        if not self.start_paused:
            self.rocket.start()
def start(self):
        """Play the music"""
        if self.initialized:
            mixer.music.unpause()
        else:
            mixer.music.play()
            # FIXME: Calling play twice to ensure the music is actually playing
            mixer.music.play()
            self.initialized = True
        self.paused = False
def get_time(self) -> float:
        """
        Get the current position in the music in seconds
        """
        if self.paused:
            return self.pause_time

        return mixer.music.get_pos() / 1000.0
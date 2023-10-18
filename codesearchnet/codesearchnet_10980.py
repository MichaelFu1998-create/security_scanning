def set_time(self, value: float):
        """
        Set the current time in the music in seconds causing the player
        to seek to this location in the file.
        """
        if value < 0:
            value = 0

        # mixer.music.play(start=value)
        mixer.music.set_pos(value)
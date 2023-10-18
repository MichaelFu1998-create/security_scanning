def draw(self, current_time, frame_time):
        """
        Calls the superclass ``draw()`` methods and checks ``HEADLESS_FRAMES``/``HEADLESS_DURATION``
        """
        super().draw(current_time, frame_time)

        if self.headless_duration and current_time >= self.headless_duration:
            self.close()
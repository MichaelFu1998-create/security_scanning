def draw(self, current_time, frame_time):
        """
        Draws a frame. Internally it calls the
        configured timeline's draw method.

        Args:
            current_time (float): The current time (preferrably always from the configured timer class)
            frame_time (float): The duration of the previous frame in seconds
        """
        self.set_default_viewport()
        self.timeline.draw(current_time, frame_time, self.fbo)
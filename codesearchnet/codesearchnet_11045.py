def set_default_viewport(self):
        """
        Calculates the viewport based on the configured aspect ratio in settings.
        Will add black borders if the window do not match the viewport.
        """
        # The expected height with the current viewport width
        expected_height = int(self.buffer_width / self.aspect_ratio)

        # How much positive or negative y padding
        blank_space = self.buffer_height - expected_height
        self.fbo.viewport = (0, blank_space // 2, self.buffer_width, expected_height)
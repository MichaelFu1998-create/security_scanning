def on_resize(self, width, height):
        """
        Pyglet specific callback for window resize events.
        """
        self.width, self.height = width, height
        self.buffer_width, self.buffer_height = width, height
        self.resize(width, height)
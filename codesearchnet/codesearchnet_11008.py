def resize(self, width, height):
        """
        Sets the new size and buffer size internally
        """
        self.width = width
        self.height = height
        self.buffer_width, self.buffer_height = glfw.get_framebuffer_size(self.window)
        self.set_default_viewport()
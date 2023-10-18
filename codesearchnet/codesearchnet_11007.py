def swap_buffers(self):
        """
        Swaps buffers, incement the framecounter and pull events.
        """
        self.frames += 1
        glfw.swap_buffers(self.window)
        self.poll_events()
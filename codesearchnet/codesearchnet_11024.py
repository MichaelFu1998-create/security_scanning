def swap_buffers(self):
        """
        Swap buffers, increment frame counter and pull events
        """
        if not self.window.context:
            return

        self.frames += 1
        self.window.flip()
        self.window.dispatch_events()
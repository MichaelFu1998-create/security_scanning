def swap_buffers(self):
        """
        Headless window currently don't support double buffering.
        We only increment the frame counter here.
        """
        self.frames += 1

        if self.headless_frames and self.frames >= self.headless_frames:
            self.close()
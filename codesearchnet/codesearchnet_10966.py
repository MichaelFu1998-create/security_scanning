def view_matrix(self):
        """
        :return: The current view matrix for the camera
        """
        # Use separate time in camera so we can move it when the demo is paused
        now = time.time()
        # If the camera has been inactive for a while, a large time delta
        # can suddenly move the camera far away from the scene
        t = max(now - self._last_time, 0)
        self._last_time = now

        # X Movement
        if self._xdir == POSITIVE:
            self.position += self.right * self.velocity * t
        elif self._xdir == NEGATIVE:
            self.position -= self.right * self.velocity * t

        # Z Movement
        if self._zdir == NEGATIVE:
            self.position += self.dir * self.velocity * t
        elif self._zdir == POSITIVE:
            self.position -= self.dir * self.velocity * t

        # Y Movement
        if self._ydir == POSITIVE:
            self.position += self.up * self.velocity * t
        elif self._ydir == NEGATIVE:
            self.position -= self.up * self.velocity * t

        return self._gl_look_at(self.position, self.position + self.dir, self._up)
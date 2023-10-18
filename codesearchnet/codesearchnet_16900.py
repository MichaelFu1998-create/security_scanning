def update(self, dt):
        """Update the shape's position by moving it forward according to its velocity.

        Parameters
        ----------
        dt : float

        """
        self.translate(dt * self.velocity)
        self.rotate(dt * self.angular_velocity)
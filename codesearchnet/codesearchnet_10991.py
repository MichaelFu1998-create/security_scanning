def draw(self, time: float, frametime: float, target: moderngl.Framebuffer):
        """
        Draw function called by the system every frame when the effect is active.
        This method raises ``NotImplementedError`` unless implemented.

        Args:
            time (float): The current time in seconds.
            frametime (float): The time the previous frame used to render in seconds.
            target (``moderngl.Framebuffer``): The target FBO for the effect.
        """
        raise NotImplementedError("draw() is not implemented")